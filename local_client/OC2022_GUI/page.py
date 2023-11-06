# -*- coding: utf-8 -*-
#This is Prototype StyleCariGAN-GUI code.

import tkinter as tk
import tkinter.ttk as ttk

class Page:
    def __init__(self, root, route, img_path, pic_size):
        self.img_path = img_path
        #ページ遷移用フラグ
        self.ready_mode = -1 #遷移先のp_numを示す
        self.route = route

        # メインフレームの作成と設置
        self.frame = ttk.Frame(root)
        self.frame.grid(row=0, column=0, sticky="nsew")
        
        self.pic_size = pic_size
        self.pic_canvas = tk.Canvas(self.frame, width=self.pic_size, height=self.pic_size, bg="#deb887")
        
        self.widgets = []
        # 各種ウィジェットの作成
        self.widgets.append(tk.Label(self.frame, text="StyleGAN", font=("MSゴシック", "20", "bold"), anchor=tk.CENTER, foreground='#4169e1'))

    def draw_widget(self, pack_mode):
        for i in range(len(self.widgets)):
            if len(pack_mode) > 0 and i > 0:
                if pack_mode[i-1] == 0:
                    self.widgets[i].pack()
                elif pack_mode[i-1] == 1:
                    self.widgets[i].pack(fill = 'x', padx=200)
                elif pack_mode[i-1] == 2:
                    self.widgets[i].pack(pady = 60)
            else:
                self.widgets[i].pack()

    def get_status(self):
        return self.ready_mode

    def reset_page(self):
        self.ready_mode = -1

    def raise_page(self):
        self.frame.tkraise()
