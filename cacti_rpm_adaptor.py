#!/usr/bin/python

# robert< at >packetflare.net 

# An adaptor to the Juniper RPM module for Cacti for use as either as a Data Input Method or as a Data Query

import argparse
import getopt
import sys

from junos_rpm import RpmCollector

def main(args) :
	rpm = RpmCollector(args.hostname, args.community)

	# <arg_index>--indexes</arg_index>
	if args.indexes is True :
		table = rpm.traverse_table_indexes(rpm.jnxPingLastTestResultProbeResponses)
		for row in table :
			print row['index_oid']

	# <arg_query>--query</arg_query>
	elif args.query :
		table = rpm.traverse_table_indexes(rpm.jnxPingLastTestResultProbeResponses)
		if args.query == 'indexes' :
			for row in table :
				index = row['index_oid']
				print '%s|%s' % (index, index)
		if args.query == 'probe_names' :
			for row in table :
				print '%s|%s-%s' % (row['index_oid'], row['probe'], row['test'])

	# <arg_get>--get</arg_get>			
	if args.get :
		if args.get == 'host_up' :
			rpm.do_walk(rpm.jnxPingLastTestResultProbeResponses, args.remainder[0])
			if rpm.count_entries > 0 :
				result = int(rpm.entries[0][1])
				if result > 1 :
					result = 1
				sys.stdout.write(str(result))
		else :
			rpm.do_walk(args.get, args.remainder[0])
			#print (args.get, args.remainder[0])
			if not rpm.error : 
				result = rpm.entries[0][1]
				sys.stdout.write(str(result))
			else :
				print 'error'

	# <arg_num_indexes>--count</arg_num_indexes>
	elif args.count is True :
		print rpm.count_entries()

	# --table 
	elif args.table is True :
		table = rpm.traverse_table_indexes(rpm.jnxPingLastTestResultProbeResponses)
		for row in table :
			print '%s-%s:%s' % (row['probe'], row['test'], row['index_oid'])
 
 	# --test and --probe
	elif args.test and args.probe :
		result = rpm.probe_result(args.probe,args.test)
		print 'name:%s-%s up:%s rtt:%s' % (args.probe, args.test, result[0], result[1])


if __name__ == '__main__' :
	parser = argparse.ArgumentParser(description='JunOS RPM monitor utility')
	parser.add_argument('-H', '--hostname', help="hostname or IP address of Juniper device to monitor", required=True)
	parser.add_argument('-c', '--community', help="SNMP community", required=True)
	parser.add_argument('-v', '--version', help="SNMP version", default='2c')
	parser.add_argument('-i', '--indexes', help="list indexes", action='store_true' )
	parser.add_argument('-q', '--query', help="Run query")
	parser.add_argument('-g', '--get', help="Run get")
	parser.add_argument('-t', '--test', help="RPM test name")	
	parser.add_argument('-p', '--probe', help="RPM probe name")	

	parser.add_argument('-C', '--count', help="Return of probe-test pairs", action='store_true')		
	parser.add_argument('-T', '--table', help="Return table indexes in ascii and oid", action='store_true')
	parser.add_argument('remainder', nargs=argparse.REMAINDER)	
	args = parser.parse_args()
	#print args
	main(args)
