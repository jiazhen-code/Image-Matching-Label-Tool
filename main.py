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
    def setSize(self, img_w, img_h):
        self.img_w = img_w
        self.img_h = img_h
        self.aligned.setScaledContents(True)
        self.resize(3 * self.img_w + 80, self.img_h + 70)
        self.raw.setGeometry(QtCore.QRect(20, 40, 2 * self.img_w+10, self.img_h+10))

        # self.pushButton.setGeometry(QtCore.QRect(190, self.img_h+90, 112, 32))
        # self.pushButton_2.setGeometry(QtCore.QRect(340, self.img_h + 90, 112, 32))
        self.label_2.setGeometry(QtCore.QRect(self.img_w + self.img_w // 7, 5, 101, 41))
        self.label_3.setGeometry(QtCore.QRect(self.img_w + self.img_w // 2, 5, 201, 41))
        self.label_3.setText('关键点对数量：')
        self.checkBox.setGeometry(QtCore.QRect(self.img_w // 2, 5, 151, 41))
        self.aligned.setGeometry(QtCore.QRect(self.img_w * 2 + 60, 40, self.img_w+10, self.img_h+10))
        self.label.setGeometry(QtCore.QRect(self.img_w * 2 + 60, 20, 81, 16))

    def __init__(self):
        super(firstForm, self).__init__()
        self.setupUi(self)

        # self.setMouseTracking(True)
        # self.raw.setMouseTracking(True)
        # self.rel.setMouseTracking(True)
        self.setWindowTitle('demo')
        self.w = 300
        self.h = 300
        # 鼠标绘图流程:1，建立Qpixmap绘图面板2，将面板加入到绘制到主界面3，定义鼠标函数和绘制函数绘制到绘图面板
        self.setSize(self.w, self.h)
        #这里可以设置显示图片的大小

        self.checkBox.setChecked(True)
        self.open=False
        self.is_raw = True
        self.imageDir = 'image/'
        self.user = 'check'
        self.save = f'save/{self.user}'
        self.work_file = f'worklist_{self.user}.txt'
        self.first_dir = os.path.join(self.imageDir, 'query')
        self.second_dir = os.path.join(self.imageDir, 'refer')
        self.scale = 1
        # self.save_first_dir = os.path.join(self.save, 'cfp')
        # self.save_second_dir = os.path.join(self.save, 'ago')
        # self.choose_save()
        self.choose_image()
        self.setMouseTracking(True)

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

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0 and self.scale >= 4:  # 只能放大4倍
            return

        else:
            scale = self.scale
            if delta > 0:
                scale *= 1.1  # 每次放大10%
            else:
                scale *= 0.9  # 每次缩小10%
            if scale <= 1:
                self.scale = 1
            else:
                self.scale = scale
                # 移动值：x * scale * 1.3 - x * scale = x * scale * 0.3
                # if delta > 0:
                #     # moveBy指的是item左上角移动的相对距离，相对原始左上角，原始值为(0, 0)向上向右为负数
                #     self.moveBy(event.pos().x(), event.pos().y(), -1)
                # else:
                #     self.moveBy(event.pos().x(), event.pos().y(), -1)
            self.setSize(int(self.w*self.scale), int(self.h*self.scale))
            self.saveOne()
            self.loadImage(self.is_raw)
            self.update()

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
        # result.show()
        if result.mode == "RGB":
            result = result.convert("RGBA")
        result = result.toqpixmap()
        # print(result)
        #

        # item1 = QGraphicsPixmapItem(rawIm)
        # item2 = QGraphicsPixmapItem(relIm)

        scene = GraphicsScene(self.img_w, result, self.img_w, self.img_h, rawIm, relIm, self.aligned)
        scene.changeValue.connect(self.setKpn)
        scene.changePage.connect(self.changePage)
        scene.addPixmap(result)# 创建场景
        save_path = self.save
        rel_name = os.path.split(relPath)[-1].split('.')[0]
        raw_name = os.path.split(rawPath)[-1].split('.')[0]
        scene.loadPair(save_path, raw_name, rel_name)

        if os.path.exists(os.path.join(save_path, raw_name+'-'+rel_name+'.txt')):
            with warnings.catch_warnings():

                warnings.simplefilter('ignore')
                save_np = np.loadtxt(os.path.join(save_path, raw_name+'-'+rel_name+'.txt'))
                self.label_3.setText(f'关键点对数量：{len(save_np)}')
        else:
            self.label_3.setText(f'关键点对数量：{0}')
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
    def setKpn(self, l):
        self.label_3.setText(f'关键点对数量：{l}')
        self.saveOne()
    def saveOne(self):
        rawPath, relPath = self.imageList[self.cur - 1]
        self.raw.scene().savePair(self.save, os.path.split(rawPath)[-1].split('.')[0], os.path.split(relPath)[-1].split('.')[0])

    def changePage(self, flag):
        if not self.open:
            return
        if len(self.imageList) > 0:
            #向前翻页
            if (flag == 1):
                self.aligned.clear()
                self.saveOne()
                self.cur = self.cur-1
                if self.cur == 0:
                    self.cur = len(self.imageList)
                self.loadImage(self.is_raw)
            elif (flag == 2):
                self.saveOne()
                self.aligned.clear()
                self.cur = self.cur+1
                if self.cur == len(self.imageList)+1:
                    self.cur = 1
                self.loadImage(self.is_raw)
            elif (flag == 3):
                self.saveOne()

class GraphicsScene(QGraphicsScene):
    changeValue = pyqtSignal(int)
    changePage = pyqtSignal(int)
    def __init__(self, width, image, img_w, img_h, raw_img, rel_img, aligned):
        super(QGraphicsScene, self).__init__()
        self.point = [[], []]
        self.choose = None
        self.width = width
        #0 代表选择的是原图上的点， 1为映射图上的点
        self.flag = None
        self.image = image
        self.sz = self.width//40
        self.w = img_w
        self.h = img_h
        self.m_x = 0
        self.m_y = 0
        self.raw_img = raw_img
        self.rel_img = rel_img
        self.aligned = aligned

        # self.addPixmap(image)

    def loadPair(self, save_path, raw_name, rel_name):
        # return
        if os.path.exists(os.path.join(save_path, raw_name+'-'+rel_name+'.txt')):
            with warnings.catch_warnings():

                warnings.simplefilter('ignore')
                save_np = np.loadtxt(os.path.join(save_path, raw_name+'-'+rel_name+'.txt'))
                if len(save_np)==0:
                    return

                if len(save_np.shape) == 1:
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

                except Exception as e:
                    print(str(e))
                    # pass
            # if len(self.point) != 0:
            #     self.changeValue.emit(len(self.point[0]))
            # else:
            #     self.changeValue.emit(0)
    def draw(self):
        pen = QPen(QtCore.Qt.blue, 2)
        pen2 = QPen(QtCore.Qt.yellow, 2)
        pen_wrong = QPen(QtCore.Qt.red, 2)
        brush = QBrush(QtCore.Qt.blue)
        brush2 = QBrush(QtCore.Qt.yellow)
        brush_wrong = QBrush(QtCore.Qt.red)

        sz = self.sz
        self.clear()
        self.addPixmap(self.image)
        msz = 3
        mask = np.ones(len(self.point[0]))
        if len(self.point[0])>=4:
            p1 = self.point[0]
            p2 = self.point[1]
            # cv_kpts1 = [cv2.KeyPoint(int(i[0]), int(i[1]), 25)
            #             for i in p1]
            # cv_kpts2 = [cv2.KeyPoint(int(i[0] - self.width), int(i[1]), 25)
            #             for i in p2]
            # src_pts = np.float32([cv_kpts1[i].pt for i in range(len(self.point[0]))]).reshape(-1, 1, 2)
            # dst_pts = np.float32([cv_kpts2[i].pt for i in range(len(self.point[0]))]).reshape(-1, 1, 2)

            src_pts = np.float32([[p1[i][0], p1[i][1]] for i in range(len(self.point[0]))]).reshape(-1, 1, 2)
            dst_pts = np.float32([[p2[i][0] - self.width, p2[i][1]] for i in range(len(self.point[0]))]).reshape(-1, 1, 2)

            H_m, mask = cv2.findHomography(src_pts, dst_pts, cv2.LMEDS, 5)

            src_pts[:, 0, 0] = src_pts[:, 0, 0] / self.w * 600
            src_pts[:, 0, 1] = src_pts[:, 0, 1] / self.h * 600

            dst_pts[:, 0, 0] = dst_pts[:, 0, 0] / self.w * 600
            dst_pts[:, 0, 1] = dst_pts[:, 0, 1] / self.h * 600
            _, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC)
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

        if self.choose is not None:
            self.addRect(self.choose[0]-sz/2, self.choose[1]-sz/2, sz, sz, pen2)
            self.addEllipse(self.choose[0]-msz/2, self.choose[1]-msz/2, msz, msz, pen2, brush2)
        for s, (x, y) in enumerate(self.point[0]):
            if mask[s]:
                self.addRect(x-sz/2, y-sz/2, sz, sz, pen)
                self.addEllipse(x - msz / 2, y - msz / 2, msz, msz, pen, brush)
            else:
                self.addRect(x - sz / 2, y - sz / 2, sz, sz, pen_wrong)
                self.addEllipse(x - msz / 2, y - msz / 2, msz, msz, pen, brush_wrong)
        for s, (x, y) in enumerate(self.point[1]):
            if mask[s]:
                self.addRect(x-sz/2, y-sz/2, sz, sz, pen)
                self.addEllipse(x - msz / 2, y - msz / 2, msz, msz, pen, brush)
            else:
                self.addRect(x - sz / 2, y - sz / 2, sz, sz, pen_wrong)
                self.addEllipse(x - msz / 2, y - msz / 2, msz, msz, pen, brush_wrong)
        for i in range(len(self.point[0])):
            qp1 = QPoint(int(self.point[0][i][0]), int(self.point[0][i][1]))
            qp2 = QPoint(int(self.point[1][i][0]), int(self.point[1][i][1]))
            ql = QLineF(qp1, qp2)
            if mask[i]:
                self.addLine(ql, pen,)

            else:
                self.addLine(ql, pen_wrong, )
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Right or QKeyEvent.key() == Qt.Key_Down or QKeyEvent.key() == Qt.Key_Left or QKeyEvent.key() == Qt.Key_Up:
            if self.choose is not None:
                up_x, up_y = self.choose
                rgw = [0, self.w - 1]
                rgh = [0, self.h - 1]
                if not self.flag:
                    rgw = [self.w, 2 * self.w - 1]
                if QKeyEvent.key() == Qt.Key_Right:
                    up_x = up_x + 1 if up_x + 1 < rgw[1] else rgw[1]
                    self.choose = [up_x, up_y]
                elif QKeyEvent.key() == Qt.Key_Left:
                    up_x = up_x - 1 if up_x - 1 > rgw[0] else rgw[0]
                    self.choose = [up_x, up_y]
                elif QKeyEvent.key() == Qt.Key_Up:
                    up_y = up_y - 1 if up_y - 1 > rgh[0] else rgh[0]
                    self.choose = [up_x, up_y]
                else:
                    up_y = up_y + 1 if up_y + 1 < rgh[1] else rgh[1]
                    self.choose = [up_x, up_y]
                self.draw()
            else:
                x, y = self.m_x, self.m_y
                # print(x, y)
                flag = x < self.width
                ps = self.point[1 - int(flag)]
                up = None
                for step, (xx, yy) in enumerate(ps):
                    # 在矩形范围内，一次删除一个点
                    if abs(x - xx) < self.sz and abs(y - yy) < self.sz:
                        up = step
                        break

                rgw = [0, self.w-1]
                rgh = [0, self.h-1]
                if not flag:
                    rgw = [self.w, 2*self.w - 1]
                if up is not None:
                    up_x, up_y = self.point[1 - flag][up]
                    if QKeyEvent.key() == Qt.Key_Right:
                        up_x = up_x + 1 if up_x + 1 < rgw[1] else rgw[1]
                        self.point[1 - flag][up] = [up_x, up_y]
                    elif QKeyEvent.key() == Qt.Key_Left:
                        up_x = up_x - 1 if up_x - 1 > rgw[0] else rgw[0]
                        self.point[1 - flag][up] = [up_x, up_y]
                    elif QKeyEvent.key() == Qt.Key_Up:
                        up_y = up_y - 1 if up_y - 1 > rgh[0] else rgh[0]
                        self.point[1 - flag][up] = [up_x, up_y]
                    else:
                        up_y = up_y + 1 if up_y + 1 < rgh[1] else rgh[1]
                        self.point[1 - flag][up] = [up_x, up_y]
                    self.changeValue.emit(len(self.point[0]))
                    self.draw()

        else:
            if QKeyEvent.key() == Qt.Key_A:
                self.changePage.emit(1)
            elif QKeyEvent.key() == Qt.Key_D:
                self.changePage.emit(2)
            elif QKeyEvent.key() == Qt.Key_S:
                self.changePage.emit(3)

    def mouseMoveEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.m_x = x
        self.m_y = y
    # def h
    def mousePressEvent(self, event):
        #鼠标左键是画点
        if event.buttons() == QtCore.Qt.LeftButton:
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
                    self.changeValue.emit(len(self.point[0]))
                else:
                    self.choose = choose
                    self.flag = flag
            else:
                self.choose = choose
                self.flag = x < self.width

                # 遍历寻找相近点修改
                flag = x < self.width
                ps = self.point[1 - int(flag)]
                up = None
                for step, (xx, yy) in enumerate(ps):
                    # 在矩形范围内，一次删除一个点
                    if abs(x - xx) < self.sz and abs(y - yy) < self.sz:
                        up = step
                        break
                if up is not None:
                    self.point[1-self.flag][up] = self.choose
                    self.choose = None
                    self.changeValue.emit(len(self.point[0]))

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
                    self.changeValue.emit(len(self.point[0]))

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