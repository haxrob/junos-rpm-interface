#!/usr/bin/python

 """   Copyright (C) 2014 robert< at >packetflare.net 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
from subprocess import Popen, PIPE
import shlex
import re

SNMP_WALK_PATH = '/usr/bin/snmpwalk'

class RpmCollector :
	
	hostname = ''
	community = ''
	walk_cmd = ''
	get_cmd = ''
	entries = []
	error = False

	jnxPingLastTestResultEntry = '1.3.6.1.4.1.2636.3.7.1.5'
	jnxPingLastTestResultProbeResponses = jnxPingLastTestResultEntry + '.1.1'
	jnxPingLastTestResultMaxRttUs = jnxPingLastTestResultEntry + '.1.5'

	def __init__(self, hostname, community = 'public', snmp_version = '2c') :
		self.walk_cmd =  '%s -c %s -On -v %s %s' % (SNMP_WALK_PATH, community, snmp_version, hostname)

	# Snmp walk on concatination of table_oid and index_oid. The is parsed stored in entries 
	# table. First element of the entry is the oid, the second is the result

	def do_walk(self, table_oid, index_oid = '') :

		self.table_oid = table_oid

		snmp_walk = '%s %s' % (self.walk_cmd, table_oid + index_oid)

		
		args = shlex.split(snmp_walk)
		proc = Popen(args, stdout=PIPE, stderr=PIPE)
		stdout, stderr = proc.communicate()
		exitcode = proc.returncode		
		#print stdout, stderr

		if (exitcode != 0) :
			sys.exit('error')

		self.__compile_snmp_walk(stdout)

	# parse snmpwalk output into table object
	def __compile_snmp_walk(self, output) :

		#split oid and result
		self.entries = [ re.split(" = \w+: ", x) for x in output.splitlines() ]

		# check if any error
		for entry in self.entries :
			if re.search('No Such Instance', entry[0]) :
				self.error = True
			

	# Walk jnxPingLastTestResultProbeResponses to determine how many probe-test pairs
	# is configured in the device.
	# Returns size of table

	def count_entries(self) :
		self.do_walk(self.jnxPingLastTestResultProbeResponses)
		return len(self.entries)


	# Returns a list of each probe-test configured in device with the respective
	# snmp oid. Each element is a dict with the keys 'probe', 'test', 'oid_index'    

	def traverse_table_indexes(self, table_oid) :

		self.do_walk(table_oid)
		
		table = []

		for entry in self.entries :
			stripped = entry[0].split(table_oid)[1]
			row = self.__oid_to_ascii(entry[0])
			row['index_oid'] = stripped
			table.append(row)

		return table

	# Runs snmp result for specified probe and test. 
	# Returns list if the respective 'host' is up and the RTT

	def probe_result(self, probe_name, test_name) :
		probe_oid = self.__ascii_to_oid(probe_name, test_name)
		
		self.do_walk(self.jnxPingLastTestResultProbeResponses, probe_oid)
		ping_result = self.entries[0]

		if int(ping_result[1]) > 1 :
			ping_result[1] = 1

		self.do_walk(self.jnxPingLastTestResultMaxRttUs, probe_oid)
		rtt_result = self.entries[0]

		return [ ping_result[1], rtt_result[1] ]

		#print self.oid_to_ascii(rtt_result[0]), rtt_result[1]	

	# Extract RPM owner and test strings from OID
	# Returns dict with the probe name and test name in ASCII format

	def __oid_to_ascii(self, oid) :

		# remove prefixed 'jnxPingLastTestResultProbeResponses' from oid 
		stripped = oid.split(self.table_oid)[1]

		if stripped[3:19] == 'No Such Instance' :
			print 'error'
			return

		# first byte is length of owner string followed by the actual owner string
		# .. then the length of the test string followed by the actual test string

		# dotted notation ..
		parts = stripped[1:].split('.')

		probe_len = int(parts[0])
		probe_str = parts[1:probe_len+1]
		test_len = int(parts[probe_len+1:probe_len+2][0])
		test_str = parts[probe_len+2:probe_len+2+test_len]

		# integer to character to string
		probe = ''.join([ chr(int(a)) for a in probe_str ])
		test = ''.join([ chr(int(a)) for a in test_str ])

		return { 'probe' : probe, 'test' : test }
	
	# Returns RPM oid index format from specified probe and test strings 

	def __ascii_to_oid(self, probe_str, test_str) :
		
		oid = ''
		probe_len = len(probe_str)
		test_len = len(test_str)

		probe_dec = ''.join([ '.' + str(ord(x)) for x in list(probe_str) ])
		test_dec =  ''.join([ '.' + str(ord(x)) for x in list(test_str) ])
		
		oid = '.%s%s.%s%s' % (probe_len, probe_dec, test_len, test_dec)
		return oid




