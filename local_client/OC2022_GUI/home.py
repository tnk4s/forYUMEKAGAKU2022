# -*- coding: utf-8 -*-
#This is Prototype StyleCariGAN-GUI code.

import tkinter as tk
import tkinter.ttk as ttk
import cv2
from PIL import ImageTk
from PIL import Image
import time

from page import Page

class Home(Page):
    def __init__(self, root, route, img_path, pic_size):
        super().__init__(root, route, img_path, pic_size)#450

        #カメラ接続
        self.deviceid = 0 # it depends on the order of USB connection. 
        self.capture = cv2.VideoCapture(self.deviceid)
        self.shooted_flag = False

        #ボタン用テキスト
        self.text = tk.StringVar(self.frame)
        self.text.set('shoot')

        # 各種ウィジェットの作成　順番を間違えるなよ
        self.widgets.append(tk.Label(self.frame, text="Please stand in front of the webcam.", font=("MSゴシック", "20"), anchor=tk.CENTER))
        self.widgets.append(tk.Button(self.frame, textvariable=self.text,  font=("MSゴシック", "50", "bold"), command=self._shoot))
        self.widgets.append(self.pic_canvas)

        # 各種ウィジェットの設置
        pack_modes = []
        super().draw_widget(pack_modes)
        
        self.show_cam()
        self.draw_update()

    def _shoot(self):
        org_img = Image.open(self.img_path + 'capture.png')
        trim_img = self._crop_center(org_img, self.pic_size, self.pic_size).resize((256, 256))
        trim_img.save(self.img_path + 'face.png', quality=100)
        self.text.set('saving')
        self.shooted_flag = True
        #capture.release()
        #v2.destroyAllWindows()

    def show_cam(self):
        ret, pf = self.capture.read()
        pf = cv2.flip(pf, 1)
        cv2.imwrite(self.img_path + 'capture.png', pf)
        self.img = ImageTk.PhotoImage(file = self.img_path + 'capture.png')
        self.pic_canvas.create_image(self.pic_size/2, self.pic_size/2, image=self.img)
    
    def draw_update(self):
        if self.shooted_flag:
            self.text.set("shoot")
            self.shooted_flag = False
            self.ready_mode = self.route[1]
    
    def _crop_center(self, pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

    def reset_page(self):
        time.sleep(0.5)
        super().reset_page()