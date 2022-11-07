
import Ui_MPRtest
import pyqtgraph as pg
import sys,time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np

import img_file

class mywindow(QtWidgets.QMainWindow,QComboBox,Ui_MPRtest.Ui_MainWindow):
    set_ini=pyqtSignal(str)

    def __init__(self):
        super(mywindow, self).__init__()
        
        self.setupUi(self)
        self.resize(1270, 900)

        self.axial=80
        self.coronal=256
        self.sagittal=256

        self.axial_win = pg.GraphicsLayoutWidget()
        self.coronal_win = pg.GraphicsLayoutWidget()
        self.sagittal_win = pg.GraphicsLayoutWidget()
        self.Axial_horizontalLayout.addWidget(self.axial_win)
        self.Coronal_horizontalLayout.addWidget(self.coronal_win)
        self.Sagittal_horizontalLayout.addWidget(self.sagittal_win)


        self.splitter_3.setSizes([100, 0])
        self.test1.clicked.connect(self.roi)

        f,self.images_raw = img_file.read_images(r"./Database/")

        self.test2.clicked.connect(self.test2_def)
        self.imgshow()


    def roi(self):

        self.lnfinite_Vertical=pg.InfiniteLine(angle=0, movable=True, pen=(255,0,0),hoverPen=(255,0,0),bounds=[-160,0])
        self.lnfinite_Horizontal=pg.InfiniteLine(angle=90, movable=True, pen=(0,255,0),hoverPen=(0,255,0),bounds=[0,160])   # 
        self.axial_img.addItem(self.lnfinite_Vertical)
        self.axial_img.addItem(self.lnfinite_Horizontal)
        # 实时更新
        self.lnfinite_Vertical.sigPositionChanged.connect(self.update)
        
    def update(self):
      print(np.abs(int(self.lnfinite_Vertical.value())))
      # self.axial=self.axial+1
      mpr_images = self.slicer(np.abs(int(self.lnfinite_Vertical.value())), self.coronal, self.sagittal, self.images_raw)
      self.axialImg_data.setImage(mpr_images[0])


    def test2_def(self):
      self.axial=self.axial+1
      mpr_images = self.slicer(self.axial, self.coronal, self.sagittal, self.images_raw)
      self.axialImg_data.setImage(mpr_images[0])

    def slicer(self,axial, coronal, sagittal, images):
      axial_image = images[axial]
      coronal_image = []
      sagittal_image = []
      for i in images:
          coronal_image.append(i[coronal])
      return [axial_image, coronal_image, sagittal_image]

    def imgshow(self):

      mpr_images = self.slicer(self.axial, self.coronal, self.sagittal, self.images_raw)

      axial_Layout = self.axial_win.addLayout(row=0, col=0)
      self.axial_labels=axial_Layout.addLabel(row=0, col=0)
      self.axial_labels.setText("", color='ffffff')
      axial_Layout.setContentsMargins(0,0,0,0)
      self.axial_img = axial_Layout.addViewBox(row=1, col=0,lockAspect=True)
      self.axialImg_data = pg.ImageItem(mpr_images[0])
      self.axialImg_data.rotate(-90)
      self.axial_img.addItem(self.axialImg_data)
      self.axial_img.setMenuEnabled(False)   # 禁用右键菜单

    

if __name__ == '__main__':

  QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
  app = QtWidgets.QApplication(sys.argv)
  main_window = mywindow()
  main_window.show()

  sys.exit(app.exec_())