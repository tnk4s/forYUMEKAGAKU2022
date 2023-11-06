# -*- coding: utf-8 -*-
#This is Prototype StyleCariGAN-GUI code.

import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk

from page import Page

class ConfirmFace(Page):
    def __init__(self, root, route, img_path, pic_size):
        #self.pic_size = 300
        super().__init__(root, route, img_path, pic_size)

        self.ytext = tk.StringVar(self.frame)
        self.ytext.set('Yes!')
        self.ntext = tk.StringVar(self.frame)
        self.ntext.set('No!!')
        
        # 各種ウィジェットの作成
        self.widgets.append(tk.Label(self.frame, text="Generates an age-modified image, is that OK?", font=("MSゴシック", "20"), anchor=tk.CENTER))
        self.widgets.append(tk.Button(self.frame, textvariable=self.ytext,  font=("MSゴシック", "40", "bold"), command=self._understand))
        self.widgets.append(tk.Button(self.frame, textvariable=self.ntext,  font=("MSゴシック", "40", "bold"), command=self._back))
        self.widgets.append(self.pic_canvas)
        
        # 各種ウィジェットの設置
        pack_modes = [0, 1, 1, 2]
        super().draw_widget(pack_modes)
        
        #顔写真描画
        self._draw_face()

    def _draw_face(self):
        self.img = ImageTk.PhotoImage(file = self.img_path + 'face.png')
        self.pic_canvas.create_image(self.pic_size/2, self.pic_size/2, image=self.img)

    def _understand(self):
        self.ready_mode = self.route[1]
    
    def _back(self):
        self.ready_mode = self.route[0]

    def raise_page(self):
        #print('raise cf')
        self._draw_face()
        super().raise_page()

