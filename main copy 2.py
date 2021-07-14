import rapidxml
from cpe import CPE
from cpe.cpeset2_2 import CPESet2_2
from cpe.cpelang2_2 import CPELanguage2_2

def get_methods(object, spacing=20):
  methodList = []
  for method_name in dir(object):
    try:
        if callable(getattr(object, method_name)):
            methodList.append(str(method_name))
    except:
        methodList.append(str(method_name))
  processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
  for method in methodList:
    try:
        print(str(method.ljust(spacing)) + ' ' +
              processFunc(str(getattr(object, method).__doc__)))
    except:
        print(method.ljust(spacing) + ' ' + ' getattr() failed')



class CPEAnalyser:
    #Loads the database, CPE/XML Format
    def __init__(self,dbPath):
        self.vendorMap = {}
        self.productMap = {}
        self.softwareTargetMap = {}
        self.hardwareTargetMap = {}
        self.hardwareTargetMap = {}
        self.languageMap = {}
        self.versionMap = {}
        self.wordToVendorMap = {}
        self.wordToProductMap = {}
        self.wordToSoftwareTargetMap = {}
        self.wordToHardwareTargetMap = {}
        
        self.cpeList = []
        with open(dbPath, 'r', encoding='utf-8') as file:
            data = file.read()
            r = rapidxml.RapidXml(data) # parsing from bytes
            cpeList = r.first_node("cpe-list") # get first node named test
            n = cpeList.first_node() 
            while(True):
                a = n.first_attribute()
                while (a):
                    if ( a.name == "name" ):
                        cpe = a.value
                        CPEOBJ = CPE(cpe)

                        cpe_dict = list(CPEOBJ.values())[0][0]
                        self.cpeList.append(cpe_dict)
                        id = len(self.cpeList)-1

                        vendor = CPEOBJ.get_vendor()[0]
                        product = CPEOBJ.get_product()[0]
                        software_target = CPEOBJ.get_target_software()[0]
                        hardware_target = CPEOBJ.get_target_hardware()[0]

                        vendorCpes  = self.vendorMap.get(vendor)
                        productCpes = self.productMap.get(product)
                        softwareTargetCpes = self.softwareTargetMap.get(software_target)
                        hardwareTargetCpes = self.hardwareTargetMap.get(hardware_target)
                        
                        if (len(vendor) and vendorCpes is None):
                            for w in self.splitName(vendor):
                                self.wordToVendorMap[w] =  [ *(  self.wordToVendorMap.get(w) or []) , vendor]

                        if (len(product) and productCpes is None):
                            for w in self.splitName(product):
                                self.wordToProductMap[w] =  [ *(  self.wordToProductMap.get(w) or []) , product]
                        
                        if (len(software_target ) and softwareTargetCpes is None):
                            for w in self.splitName(software_target):
                                self.wordToSoftwareTargetMap[w] =  [ *(  self.wordToSoftwareTargetMap.get(w) or []) , software_target]
                        
                        if (len(hardware_target) and hardwareTargetCpes is None):
                            for w in self.splitName(hardware_target):
                                self.wordToHardwareTargetMap[w] =  [ *(  self.wordToHardwareTargetMap.get(w) or []) , hardware_target]
                        
                        self.vendorMap[vendor]                      = [ *(  vendorCpes or []) , id]
                        self.productMap[product]                    = [ *(productCpes or []) , id]
                        self.softwareTargetMap[software_target]     = [ *( softwareTargetCpes or []) , id]
                        self.hardwareTargetMap[hardware_target]     = [ *(hardwareTargetCpes or []) , id]
                    if (a==n.last_attribute()):
                        break
                    a = a.next_attribute()
                n = n.next_sibling()
                if (n == cpeList.last_node()):
                    break
    def splitName(self , name : str):
        seperators = "-_*/.,"
        rv = [name]
        for s in seperators:
            copy = []
            for n in rv:
                copy = [ *copy , *n.split(s)]
            rv= copy
        return rv
    def collectWordData(self , w):
        return [
            *( { "ht" : i , "type" : "ht" } for i in  self.wordToHardwareTargetMap.get(w) or [] ) , 
            *( { "product" : i , "type" : "product" } for i in  self.wordToProductMap.get(w) or [] ) , 
            *( { "st" : i , "type" : "st" } for i in  self.wordToSoftwareTargetMap.get(w) or [] ) , 
            *( { "vendor" : i , "type" : "vendor" } for i in  self.wordToVendorMap.get(w) or [] ) 
        ]
    def collectCpeWordDataElement(self , elm ):
        print("elm : " , elm)
        if (elm["type"] == "ht"):
           # return self.hardwareTargetMap[elm["ht"]]
            return [self.cpeList[i] for i in self.hardwareTargetMap[elm["ht"]]]
        if (elm["type"] == "product"):
            #return self.productMap[elm["product"]]
            return ([self.cpeList[i] for i in self.productMap[elm["product"]]])
        if (elm["type"] == "st"):
           # return self.softwareTargetMap[elm["st"]]
            return ([self.cpeList[i] for i in self.softwareTargetMap[elm["st"]]])
        if (elm["type"] == "vendor"):
            #return  self.vendorMap[elm["vendor"]] 
            return ( [ self.cpeList[i] for i in self.vendorMap[elm["vendor"]] ] )
    def getCPEsOfWord(self ,w):
        data = self.collectWordData(w)
        rv = []
        for d in data:
            rv = [*rv, self.collectCpeWordDataElement(d)]
        return rv
    def getCpeOfPckg(self , pckg):
        words = self.splitName(pckg)
        print(words)
        rv = []
        for w in words:
            rv = [*rv, self.getCPEsOfWord(w)]
        return rv

mavenName = input('Enter a mavens artifact name: ')
cpeAnalyser = CPEAnalyser("./reduced/echantillion-cpe-names.xml")
#com.apache.httpclient
with open('out.txt', 'w') as f:
    print(cpeAnalyser.getCpeOfPckg(mavenName), file=f)

#print(cpeAnalyser.getCpeOfPckg("com.apache.httpclient"))