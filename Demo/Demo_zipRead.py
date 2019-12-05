import zipfile
import xml.etree.ElementTree as ET
import xml.dom.minidom

filepath = r"C:\Users\Cjay\PycharmProjects\Contour_marker\data\Material\mc-enep.kmz"
read_hey = zipfile.ZipFile(filepath)
print(read_hey.namelist())
information = read_hey.getinfo(read_hey.namelist()[0])
print(information)
content = read_hey.read(read_hey.namelist()[0])
# print(content)
#ET.fromstringlist()
root = ET.fromstring(content)
print(root.tag, ":", root.attrib)

'''for child in root:
    # 第二层节点的标签名称和属性
    print(child.tag,":", child.attrib)
    # 遍历xml文档的第三层
    for children in child:
        # 第三层节点的标签名称和属性
        print(" ",children.tag, ":", children.attrib)
        for children2 in children:
            print("  ",children2.tag, ":", children2.attrib)'''

dom = xml.dom.minidom.parseString(content)
pretty_xml_as_string = dom.toprettyxml()
print(pretty_xml_as_string)
