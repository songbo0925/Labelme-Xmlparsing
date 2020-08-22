import os
import xml.etree.ElementTree as ET
import cv2 as cv

# 图片和xml的路径
img_path = "./image"
xml_path = "./xml"
save_path = "./output"

# 读取所有xml文件并进行处理
if os.path.exists(xml_path):
    xml_files = []
    for i in os.listdir(xml_path):
        xml_files.append(i)
else:
    print("xml path error!")

for xml_files_temp in xml_files:
    # 读取xml文档
    tree = ET.ElementTree(file=os.path.join(xml_path, xml_files_temp))
    ###### 获取xml文件信息中目标ID和位置 ########
    # 新建列表
    xml_list = []
    # 获取根节点
    root = tree.getroot()
    for member in root.findall('object'):
        value = (root.find('filename').text,  # 获取图片名称
                 member[8][0][1].text,  # height min
                 member[8][2][1].text,  # height max
                 member[8][0][0].text,  # width min
                 member[8][2][0].text,  # width max
                 member[9].text[9:10]   # ID
                 )
        xml_list.append(value)

    ####### 截取目标并保存 ########
    for person_obj in xml_list:
        image = cv.imread(os.path.join(img_path, person_obj[0]))
        image_crop = image[int(float(person_obj[1])):int(float(person_obj[2])), int(float(person_obj[3])):int(float(person_obj[4]))]
        save_name = person_obj[5] + "_" + "c1" + "_" + person_obj[0]
        cv.imwrite(os.path.join(save_path, save_name), image_crop)
