## A Python interface to Juniper RPM

The [Real-time peformance monitoring](http://www.juniper.net/techpubs/software/junos-security/junos-security96/junos-security-admin-guide/rpm-ov-section.html) feature in Juniper router's and switches provides a mechanism to monitor remote hosts from the device. The RPM functionality can be accessed from the Junos [SNMP interface](http://www.juniper.net/us/en/local/pdf/app-notes/3500145-en.pdf) for use in SNMP based monitoring network devices. The way in which the probe references are encoded is not trivial, and as such many monitoring tools may require adaptations in order to fully support the decoding/indexing and retrieval of the RPM counters.

The Python module provides an easy to use interface, wrapping over snmpwalk to access the RPM probe results for use in both commercial and home-brew monitoring tools.

### Usage

Configure RPM as required in the Juniper device. Example :
```
services {
    rpm {
        probe google {
            test dns1 {
                target address 8.8.8.8;
                probe-count 3;
                probe-interval 15;
            }
            test dns2 {
                target address 8.8.4.4;
                probe-count 3;
                probe-interval 15;
            }
        }
    }
}
```

#### Fetch host status and RTT
Provide the probe and test name and return a list containing the host status (1 or 0) and the round trip time in microseconds -
```python 
>>> from ninx_rpm import RpmCollector
>>> rpm = RpmCollector('192.168.1.1', 'public')
>>> rpm.probe_result('google', 'dns1')
[1, '44420']
>>> rpm.probe_result('google', 'dns2')
[1, '38752']
```
### List all probe-test pairs and respective index OID's configured on the device -
```python
>>> table = rpm.traverse_table_indexes(rpm.jnxPingLastTestResultProbeResponses)
>>> for row in table :
...   print row
... 
{'test': 'dns1', 'probe': 'google', 'index_oid': '.6.103.111.111.103.108.101.4.100.110.115.49'}
{'test': 'dns2', 'probe': 'google', 'index_oid': '.6.103.111.111.103.108.101.4.100.110.115.50'}
```
### Query specific OID
```python
>>> rpm.do_walk(rpm.jnxPingLastTestResultProbeResponses, '.6.103.111.111.103.108.101.4.100.110.115.49')
>>> for entry in rpm.entries :
...  print entry
... 
['.1.3.6.1.4.1.2636.3.7.1.5.1.1.6.103.111.111.103.108.101.4.100.110.115.49', '3']
```

## Example implementation
```cacti_rpm_adaptor.py``` is an example implementation which can be configured as a Cacti [Data Input Method](http://docs.cacti.net/manual:087:3a_advanced_topics.1_data_input_methods) or as a [Data Query](http://docs.cacti.net/manual:087:3a_advanced_topics.3_data_queries#data_queries). 

With this implementation, the indexing and decoding of the RPM OIDs is automatic, allowing the graphing of any counter in the related Juniper RPM Mibs.

![graph](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/17.jpg)

See the following [detailed instructions](cacti-instructions/README.md) for detailed instructions.


