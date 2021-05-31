'''
本文件用于生成全部的image_pair对

'''

import os
#定义数据集文件位置
imageDir = 'image'


fs = []
for curDir, dirs, files in os.walk(imageDir):
    # print("====================")
    # print("现在的目录：" + curDir)
    # print("该目录下包含的子目录：" + str(dirs))
    # print("该目录下包含的文件：" + str(files))
    fs += [ os.path.join(curDir, x) for x in files]
imageList = []
rawL = []
relL = []
for i in fs:
    if i.endswith('.jpg'):
        if 'a' in i.split('_')[-1].replace('.jpg', ''):
            relL.append(i)
        else:
            rawL.append(i)
rd = {}
for i in relL:
    names = os.path.split(i)[-1].split('_')
    flag = names[0]+names[1]
    if flag in rd:
        rd[flag].append(i)
    else:
        rd[flag] = [i]
#构建原图和造影图对，根据文件名的前两个标识唯一
data = []
for i in rawL:
    names = os.path.split(i)[-1].split('_')
    flag = names[0] + names[1]
    if flag in rd:
        for j in rd[flag]:
            data.append((os.path.split(i)[-1].split('.')[0], os.path.split(j)[-1].split('.')[0]))

s = ''
for c, a in data:
    s += c+' '+a+'\n'

f = open('worklist.txt', 'w')
f.write(s)
f.close()