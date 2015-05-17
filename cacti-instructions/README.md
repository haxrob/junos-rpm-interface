## Graphing Juniper's Realtime Monitoring Peformance in Cacti

### Introduction

The following guideline outlines in detail how to make use of ```cacti_rpm_adaptor``` using the Data Query method in Cacti. The benefit of using Data Queries is that the RPM probes configuraiton is automatically fetched from the Juniper device and the graphs automatically created in Cacti with auto-generated names. This means that no prior knowledge of what is configured on the Juniper device is needed when creating new graphs. In effect, the graph setup is determined by what is configured in the Juniper device by parsing the OID indexes. Some might argue that the initial setup is an involved effort, but the return on investment is apparent when you have many probes configured.

## Setting it all up

### Copy source files to Cacti
(The following paths assume the default installation of Cacti on Ubuntu)

1. Place [juniper_rpm.xml](../juniper_rpm.xml) to '/usr/share/cacti/resource/script_queries/'
2. Place both [junos_rpm.py](../junos_rpm.py) and [cacti_rpm_adaptor.py](../cacti_rpm_adaptor.py) to '/usr/share/cacti/site/scripts/'

### Create Data Query

1. Select 'Data Queries' from the left hand menu and click 'Add' on the top right hand side to create a new Data Query. Fill in the parameters as shown -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/1.jpg)

2. Associate the created Data Query to the Device by selecting 'Devices' from the left hand menu and then selecting the data query to '[Juniper] RPM' and the re-index method to 'index count changed' as shown -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/2.jpg)

3. Verify that the data query works as expected by selecting 'verbose query'. The probe indexes should be extracted and decoded, similar to this example -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interfacinterface/master/cacti-instructions/images/3.jpg)

### Create Data Template

1. Select 'Data Templates' from the left hand menu and then select 'Add'. 
2. Select 'User per datasource' and enter the string  '|host_description| - |query_rpmName| RPM' in the text box
3. Select 'Get Script Data (indexed)' as the data input method -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/4.jpg)

In this example we will add two counters, 'host_up' and 'jnxPingLastTestResultAvgRttUs'. 

4. Add the data source item 'host_up' before selecting 'Create' -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/5.jpg)

5. Add a new data source item for the counter 'jnxPingLastTestResultAvgRttUs' -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/6.jpg)

6. Select all three checkboxes shown then select 'Save' -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/7.jpg)

### Create Graph Template

1. Click 'graph templates' on the right hand menu and then click 'Add' on the right hand side to create a new graph template
2. Enter a template name and enter the text '|host_description| - |query_rpmName| - RPM' in the title feild. Ensure that the respective checkbox 'use per graph value' is selected.

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/8.jpg)

3. Fill out any other respective field and click save.
4. Click 'Add' in the 'Graph Template Items' (top section)
5. Select '[Juniper] RPM Template - (jnxPingLastTestResu)' counter in the Data Source drop down box
6. Select 'Graph Item Type' to AREA

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/9.jpg)

7. Click save. Create the exact same item again, but select Graph Item Type 'LINE' with a different color
8. Add another item, this time type 'LEDGEND' on the counter. The graph template items should look similar to this -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/10.jpg)

9. The graph template needs to be associated to the graph query. Click on 'Data Queries' on the left hand menu and select the data query '[Juniper] - RPM'. Under the 'Associated Graph Templates' section, click Add.
10. Enter a name and select the Graph Template -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/11.jpg)

11. Enter in the text '|host_description| - RPM - |query_rpmName|' in the first text box, and the text 'title' in the 'field name' text box. Both these text boxes are under 'Data Template' section as shown. Click Save -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/12.jpg)

12. Enter in the text '|host_description| - RPM - |query_rpmName|' in the first text box, and the text 'name' in the 'field name' text box. Both these text boxes are under 'Graph Template' section as shown. Click Save. 

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/13.jpg)

13. Under the section 'Associated Data Templates' match the fields name and ensure both checkboxes are selected as shown -

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/14.jpg)
## Create new graphs

1. In order to graph new probes, select 'Devices' from the left hand menu. Select the Juniper device from the list and select 'Create Graphs for this Host. 
2. Select the probe that is wanted to be graph. Probes already graphed are not selectable. After selecting 'Create', the graph is automatically created.

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/15.jpg)

3. View the new graph in the graphs section under the device. As the graph is associated with the device, there is no need to manually add it under the tree.

![screenshot](https://raw.githubusercontent.com/packetflare/junos-rpm-interface/master/cacti-instructions/images/16.jpg)

## Adding new counters

There are many counters available in both the [JUNIPER-RPM-MIB](http://www.oidview.com/mibs/2636/JUNIPER-RPM-MIB.html) and [JUNIPER-PING-MIB](http://www.oidview.com/mibs/2636/JUNIPER-PING-MIB.html). In order to add support for new counters, simply add the OID to the [juniper_rpm.xml](../juniper_rpm.xml) XML file. For example if the counter 'jnxRpmResSumPercentLost' was to be graphed, the respective OID '1.3.6.1.4.1.2636.3.50.1.2.1.4' obtained from the MIB would be added as such -

```XML
    <jnxRpmResSumPercentLost>
      <name>Percent Lost</name>
      <direction>output</direction>
      <query_name>1.3.6.1.4.1.2636.3.50.1.2.1.4</query_name>
    </jnxRpmResSumPercentLost>
```

The data template has to be modified as described earlier for inclusion of the new counter.

