# Retinal-Label-Tool

## 使用需知

1. 使用前请先准备好数据文件，如image文件夹中的格式，包含两个文件夹：cfp和ago。

2. 本工具默认使用image文件夹作为数据集文件，save文件夹保存标注结果。

3. 本工具采用绝对布局，如果显示不全，可以调整[main.py](https://github.com/QzAnsel/Retinal-Label-Tool/blob/master/main.py)代码中的[self.img_w](https://github.com/QzAnsel/Retinal-Label-Tool/blob/master/main.py#L30)和[self.img_h](https://github.com/QzAnsel/Retinal-Label-Tool/blob/185ba2b16af30cf5062989cb9b085d8c78221080/main.py#L31)参数。

4. 标注时显示的是一个矩形框，实际存储的位置是该矩形框的中心位置。所以尽量使得矩形框的中心区域更接近要标注的特征点。

## 使用说明

1. 为了分配工作方便，默认读取[worklist.txt](https://github.com/QzAnsel/Retinal-Label-Tool/blob/master/worklist.txt)文件中的pair对，格式如1005_Z1812_c0 1005_Z1812_a2。该文件可通过generalize_pair.py文件自动生成，会生成该数据集全部的pair对，后续可以手动
分配worklist。

2. 开启程序时，会自动读取worklist.txt的pair对，同时默认数据集文件为image/cfp和image/ago，保存路径为save/。保存格式为x1 y1 x2 y2,分别对应cfp中关键点的x，y坐标与ago图中的x，y坐标。

3. 为了方便标注，显示原图时采用了数据增强方法，也可以选中显示原图按钮来显示原彩色图

4. 标注时可以用鼠标左键选择左图或右图中的一个区域点，此时显示的区域框为黄色，可以再次按下鼠标右键取消选中；
然后再次选中另一个图中的一个区域点，则自动产生一个匹配对连线，此时颜色变为蓝色。如果想删除某一个匹配对连线，在这个匹配对的端点区域按下鼠标右键即可删除。

5. 为了操作方便，本工具采用键盘控制翻页和保存。上翻页为键盘A，下翻页为键盘D，保存标注结果为S，注意翻页会自动保存标注结果。
