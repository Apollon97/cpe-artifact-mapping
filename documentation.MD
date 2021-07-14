CPE - aritifact mapping 
1- what is a cpe:

- dictionary ( big data )
- cpe/xml format 
    - regex r("cpe:2\\\\.3:[aho](?::(?:[a-zA-Z0-9!\\"#$%&'()*+,\\\\\\\\\\\\-_.\\\\/;<=>?@\\\\[\\\\]^`\{|\}~]|\\\\\\\\:)+)\{10\}$");
    
     -cpe:/ \{part\} : \{vendor\} : \{product\} : \{version\} : \{update\} : \{edition\} : \{language\}
     -fs                Returns the CPE Name as formatted string of version 2.3. 
     -uri_2_3           Returns the CPE Name as URI string of version 2.3. 
     -wfn               Returns the CPE Name as Well-Formed Name string of  version  2.3. 
- parsing: CPE NAME -> WORD ( CPE Library in python ) 

get                  :Return the value for key if key is in the dictionary, else default.
get_attribute_values :Returns the values of attribute "att_name" of CPE Name. By default a only element in     each part. :param string att_name: Attribute name to get :returns: List of attribute values :rtype: list :exception: ValueError - invalid attribute name
get_edition          :Returns the edition of product of CPE Name as a list. According to the CPE version, this list can contains one
or more items. :returns: Value of edition attribute as string list. :rtype: list
get_language         :Returns the internationalization information of CPE Name as a list. According to the CPE version, this list can contains one or more items. :returns: Value of language attribute as string list. :rtype: list
get_other            :Returns the other information part of CPE Name. :returns: Value of other attribute as string list. :rtype: list
get_part             :Returns the part component of CPE Name as a list. According to the CPE version, this list can contains one or more items. :returns: Value of part attribute as string list. :rtype: list
get_product          :Returns the product name of CPE Name as a list. According to the CPE version, this list can contains one or more items. :returns: Value of product attribute as string list. :rtype: list
get_software_edition :Returns the software edition of CPE Name. :returns: Value of sw_edition attribute as string list. :rtype: list
get_target_hardware  :Returns the arquitecture of CPE Name. :returns: Value of target_hw attribute as string list. :rtype: list
get_target_software  :Returns the software computing environment of CPE Name within which the product operates. :returns: Value of target_sw attribute as string list. :rtype: list
get_update           :Returns the update or service pack information of CPE Name as a list. According to the CPE version, this list can contains one or more items. :returns: Value of update attribute as string list. :rtype: list
get_vendor           :Returns the vendor name of CPE Name as a list. According to the CPE version, this list can contains one or more items. :returns: Value of vendor attribute as string list. :rtype: list
get_version          :Returns the version of product of CPE Name as a list. According to the CPE version, this list can contains one

2. ARTIFACTS:
0- Artifact types: [ Maven, JAVA, NPM, NUGGETS..]

1- Maven artifact name: 

org.apache.commons:commons-lang3:war:3.4
org.apache.commons:commons-lang3:3.4
org.apache.commons:commons-lang3:3.4-SNAPSHOT 

groupId (company / organization . name) 
: artifactId ( name of the project)
: package extension (optional) 
: version 
- isSnapshot  (optional)

MAPPING :
Construction of maps : while parsing the xml database we build two types of maps :
•	Word -> {product names, vendor names, software-target names, hardware-target names}
•	{product name , vendor name , software-target name , hardware-target name} -> CPE name

o	Product name to cpe map =  { “name1” : [ cpes id list ] , “name2” : [cpes id list ]}
o	Vendor name to cpe map =  { “name1” : [ cpes id list ] , “name2” : [cpes id list ]}
o	Software-target name to cpe map =  { “name1” : [ cpes id list ] , “name2” : [cpes id list ]}
o	Hardware-target name to cpe map =  { “name1” : [ cpes id list ] , “name2” : [cpes id list ]}
Lockup :
•	To find all CPEs related to a package , we split the package into words using string separators ( -_*/., ), for each word we lockup for all relative {products and vendors and software, hardware target … } then we use all related names to find all related Cpes to those names 

