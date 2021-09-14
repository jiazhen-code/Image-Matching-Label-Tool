import warnings

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from ui import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import numpy as np
import cv2
from PIL import Image, ImageQt
from preprocess import pre_processing

class firstForm(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(firstForm, self).__init__()
        self.setupUi(self)

        # self.setMouseTracking(True)
        # self.raw.setMouseTracking(True)
        # self.rel.setMouseTracking(True)
        self.setWindowTitle('demo')
        # 鼠标绘图流程:1，建立Qpixmap绘图面板2，将面板加入到绘制到主界面3，定义鼠标函数和绘制函数绘制到绘图面板

        #这里可以设置显示图片的大小
        self.img_w = 500
        self.img_h = 500
        self.aligned.setScaledContents(True)
        self.resize(2*self.img_w+50, 2*self.img_h+50)
        self.raw.setGeometry(QtCore.QRect(20, 40, 2*self.img_w, self.img_h))

        # self.pushButton.setGeometry(QtCore.QRect(190, self.img_h+90, 112, 32))
        # self.pushButton_2.setGeometry(QtCore.QRect(340, self.img_h + 90, 112, 32))
        self.label_2.setGeometry(QtCore.QRect(self.img_w+self.img_w//2, 5, 101, 41))
        self.checkBox.setGeometry(QtCore.QRect(self.img_w//2, 5, 151, 41))
        self.checkBox.setChecked(True)
        self.aligned.setGeometry(QtCore.QRect(self.img_w//2+30, self.img_h+70, self.img_w, self.img_h//1.2))
        self.label.setGeometry(QtCore.QRect(self.img_w//2-60, self.img_h+100, 81, 16))
        self.save = None
        self.open=False
        self.is_raw = True
        self.imageDir = 'image/'
        self.save = 'save/'
        self.work_file = 'worklist.txt'
        self.first_dir = os.path.join(self.imageDir, 'cfp')
        self.second_dir = os.path.join(self.imageDir, 'ago')

        # self.save_first_dir = os.path.join(self.save, 'cfp')
        # self.save_second_dir = os.path.join(self.save, 'ago')
        # self.choose_save()
        self.choose_image()

    def get_img_path(self, image_dir, img_id):
        return os.path.join(image_dir, '%s.jpg' % img_id)

    def loadDir(self):
        # for debug
        # self.imageDir = "./data/images"
        # self.outDir = "./data/labels"
        # self.imageList = glob.glob(os.path.join(self.imageDir, '*.png'))

        self.imageList = self.data
        # print(self.imageList)
        if len(self.imageList) == 0:
            print('No .jpg images found in the specified dir!')
            msg = QtWidgets.QMessageBox.warning(self, u'Warning', u'没有以jpg结尾的图片或无对应的造影图与原图！',
                                                buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
            return
        else:
            print("num=%d" % (len(self.imageList)))

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

        if not os.path.exists(self.save):
            os.mkdir(self.save)

        self.loadImage(self.is_raw)
        print('%d images loaded from %s' % (self.total, self.imageDir))

    def choose_image(self):
        # if self.save is None:
        #     msg = QtWidgets.QMessageBox.warning(self, u'Warning', u'请先选择存储位置！',
        #                                         buttons=QtWidgets.QMessageBox.Ok,
        #                                         defaultButton=QtWidgets.QMessageBox.Ok)
        #     return
        # directory = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        #
        # if directory == '':
        #     return


        work_file = self.work_file
        f = open(work_file, 'r')
        data = f.readlines()
        self.data = []
        for i in data:
            try:
                c, a = i.replace('\n', '').split(' ')[0], i.replace('\n', '').split(' ')[1],
                self.data.append((self.get_img_path(self.first_dir, c), self.get_img_path(self.second_dir, a)))
            except Exception:
                pass

        self.loadDir()
        self.open=True

    def show_raw(self):
        if self.checkBox.isChecked():
            self.is_raw = True
            self.saveOne()
            self.loadImage(self.is_raw)
        else:
            self.is_raw = False
            self.saveOne()
            self.loadImage(self.is_raw)

    def loadImage(self, raw_show=False):
        rawPath, relPath = self.imageList[self.cur - 1]
        rawIm = cv2.imread(rawPath, 1)
        relIm = cv2.imread(relPath, 1)
        rawIm = cv2.resize(rawIm,(self.img_w, self.img_h))
        relIm = cv2.resize(relIm, (self.img_w, self.img_h))
        result = np.zeros([self.img_h, 2*self.img_w, 3])
        result[:self.img_h, :self.img_w, :] = rawIm
        result[:self.img_h, self.img_w:, :] = relIm
        if not raw_show:
            rawIm2 = rawIm[:, :, 1]
            rawIm2 = pre_processing(rawIm2)
            rawIm2 = cv2.cvtColor(rawIm2, cv2.COLOR_GRAY2RGB)
            relIm2 = relIm[:, :, 1]
            relIm2 = pre_processing(relIm2)
            relIm2 = cv2.cvtColor(relIm2, cv2.COLOR_GRAY2RGB)

            result = np.zeros([self.img_h, 2*self.img_w, 3])
            result[:self.img_h, :self.img_w, :] = rawIm2
            result[:self.img_h, self.img_w:, :] = relIm2

        result = result.astype(np.uint8)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result = Image.fromarray(result)
        result = ImageQt.toqpixmap(result)

        # item1 = QGraphicsPixmapItem(rawIm)
        # item2 = QGraphicsPixmapItem(relIm)

        scene = GraphicsScene(self.img_w, result, self.img_w, self.img_h, rawIm, relIm, self.aligned)  # 创建场景
        scene.loadPair(self.save, os.path.split(rawPath)[-1].split('.')[0], os.path.split(relPath)[-1].split('.')[0])
        self.raw.setScene(scene)
        # self.raw.fitInView(scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        # self.rel.setScene(scene2)

        self.label_2.setText('{}/{}'.format(self.cur, len(self.data)))

    # def choose_save(self):
    #     # directory = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
    #     # if directory == '':
    #     #     self.save = None
    #     #     return
    #     directory = 'save/'
    #     self.save = directory

    def saveOne(self):
        rawPath, relPath = self.imageList[self.cur - 1]
        self.raw.scene().savePair(self.save, os.path.split(rawPath)[-1].split('.')[0], os.path.split(relPath)[-1].split('.')[0])

    def keyPressEvent(self, event):
        if not self.open:
            return
        if len(self.imageList) > 0:
            #向前翻页
            if (event.key() == Qt.Key_A):
                self.aligned.clear()
                self.saveOne()
                self.cur = self.cur-1
                if self.cur == 0:
                    self.cur = len(self.imageList)
                self.loadImage(self.is_raw)
            elif (event.key() == Qt.Key_D):
                self.saveOne()
                self.aligned.clear()
                self.cur = self.cur+1
                if self.cur == len(self.imageList)+1:
                    self.cur = 1
                self.loadImage(self.is_raw)
            elif (event.key() == Qt.Key_S):
                self.saveOne()

class GraphicsScene(QGraphicsScene):
    def __init__(self, width, image, img_w, img_h, raw_img, rel_img, aligned):
        super(QGraphicsScene, self).__init__()
        self.point = [[], []]
        self.choose = None
        self.width = width
        #0 代表选择的是原图上的点， 1为映射图上的点
        self.flag = None
        self.addPixmap(image)
        self.image = image
        self.sz = self.width//33
        self.w = img_w
        self.h = img_h
        self.raw_img = raw_img
        self.rel_img = rel_img
        self.aligned = aligned

    def loadPair(self, save_path, raw_name, rel_name):
        if os.path.exists(os.path.join(save_path, raw_name+'-'+rel_name+'.txt')):
            with warnings.catch_warnings():

                warnings.simplefilter('ignore')
                save_np = np.loadtxt(os.path.join(save_path, raw_name+'-'+rel_name+'.txt'))
                if len(save_np)==0:
                    return

                if len(save_np.shape) == 1:
                    # print(save_np.shape)
                    save_np = save_np[np.newaxis, :]

                raw = save_np[:, :2]
                rel = save_np[:, 2:]

                try:
                    raw[:, 0] *= float(self.w)
                    raw[:, 1] *= float(self.h)
                    rel[:, 0] *= float(self.w)
                    rel[:, 1] *= float(self.h)
                    rel[:, 0] += self.width
                    self.point = [list(raw), list(rel)]
                    self.draw()
                except Exception:
                    pass

    def draw(self):
        pen = QPen(QtCore.Qt.blue)
        pen2 = QPen(QtCore.Qt.yellow)
        brush = QBrush(QtCore.Qt.blue)
        brush2 = QBrush(QtCore.Qt.yellow)
        sz = self.sz
        self.clear()
        self.addPixmap(self.image)
        msz = 3
        if self.choose is not None:
            self.addRect(self.choose[0]-sz/2, self.choose[1]-sz/2, sz, sz, pen2)
            self.addEllipse(self.choose[0]-msz/2, self.choose[1]-msz/2, msz, msz, pen2, brush2)
        for x, y in self.point[0]:
            self.addRect(x-sz/2, y-sz/2, sz, sz, pen)
            self.addEllipse(x - msz / 2, y - msz / 2, msz, msz, pen, brush)
        for x, y in self.point[1]:
            self.addRect(x-sz/2, y-sz/2, sz, sz, pen)
            self.addEllipse(x - msz / 2, y - msz / 2, msz, msz, pen, brush)
        for i in range(len(self.point[0])):
            qp1 = QPoint(self.point[0][i][0], self.point[0][i][1])
            qp2 = QPoint(self.point[1][i][0], self.point[1][i][1])
            ql = QLineF(qp1, qp2)
            self.addLine(ql, pen,)

        if len(self.point[0])>=4:
            p1 = self.point[0]
            p2 = self.point[1]
            cv_kpts1 = [cv2.KeyPoint(int(i[0]), int(i[1]), 25)
                        for i in p1]
            cv_kpts2 = [cv2.KeyPoint(int(i[0] - self.width), int(i[1]), 25)
                        for i in p2]
            src_pts = np.float32([cv_kpts1[i].pt for i in range(len(self.point[0]))]).reshape(-1, 1, 2)
            dst_pts = np.float32([cv_kpts2[i].pt for i in range(len(self.point[0]))]).reshape(-1, 1, 2)
            H_m, mask = cv2.findHomography(src_pts, dst_pts, 0, 3)
            if H_m is not None:
                im1 = self.raw_img[:,:,1]
                im2 = self.rel_img[:,:,1]
                h, w = im1.shape[0], im1.shape[1]
                merged = np.zeros((h, w, 3), dtype=np.uint8)
                align_im1 = cv2.warpPerspective(im1, H_m, (h, w), borderMode=cv2.BORDER_CONSTANT, borderValue=(0))
                # print(im1.shape)
                merged[:, :, 0] = align_im1
                merged[:, :, 1] = im2
                label_width = self.aligned.width()
                label_height = self.aligned.height()
                img_src = merged
                temp_imgSrc = QImage(img_src[:], img_src.shape[1], img_src.shape[0], img_src.shape[1] * 3, QImage.Format_RGB888)
                # 将图片转换为QPixmap方便显示
                pixmap_imgSrc = QPixmap.fromImage(temp_imgSrc).scaled(label_width, label_height)
                self.aligned.setPixmap(pixmap_imgSrc)


    def mousePressEvent(self, event):
        #鼠标左键是画点
        if event.buttons () == QtCore.Qt.LeftButton:
            x = event.scenePos().x()
            y = event.scenePos().y()
            choose = [x, y]
            #如果当前已选择了一个点
            if self.choose is not None:
                flag = x < self.width
                #选择了原图和映射图中各一个点
                if flag != self.flag:
                    if flag:
                        self.point[0].append(choose)
                        self.point[1].append(self.choose)
                    else:
                        self.point[1].append(choose)
                        self.point[0].append(self.choose)
                    self.choose = None
                    self.flag = None
                else:
                    self.choose = choose
                    self.flag = flag
            else:
                self.choose = choose
                self.flag = x < self.width
        #鼠标右键是擦除
        elif event.buttons () == QtCore.Qt.RightButton:
            x = event.scenePos().x()
            y = event.scenePos().y()
            if self.choose is not None:
                self.choose = None
                self.flag = None
            else:
                #遍历寻找相近点删除
                flag = x < self.width
                ps = self.point[1-int(flag)]
                rm = None
                for step, (xx, yy) in enumerate(ps):
                # 在矩形范围内，一次删除一个点
                    if abs(x-xx) < self.sz and abs(y-yy) < self.sz:
                        rm = step
                        break
                if rm is not None:
                    del self.point[0][rm]
                    del self.point[1][rm]

        self.draw()


    def savePair(self, save_path, raw_name, rel_name):
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        raw = np.array(self.point[0])
        rel = np.array(self.point[1])
        save_np = np.zeros([len(raw), 4])
        if len(raw)!=0:
            rel[:, 0]-=self.width
            raw[:, 0] /= float(self.w)
            raw[:, 1] /= float(self.h)
            rel[:, 0] /= float(self.w)
            rel[:, 1] /= float(self.h)

            save_np[:, :2] = raw
            save_np[:, 2:] = rel
        np.savetxt(os.path.join(save_path, raw_name+'-'+rel_name+'.txt'), save_np)
        # np.savetxt(os.path.join(save_path_ago, rel_name), rel)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = firstForm()
    myshow.show()
    sys.exit(app.exec_())