# -*- coding: utf-8 -*-
#This is Prototype StyleCariGAN-GUI code.

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import cv2
import time
import subprocess

from page import Page
from g_drive_connect import GdriveConnect

class ViewResult(Page):
    def __init__(self, root, route, img_path, pic_size, gd_flag):
        super().__init__(root, route, img_path, pic_size)

        #動画用
        self.face_video = None
        self.video_frames = None
        self.video_image = None
        self.video_image_tk = None
        self.playing = False# 動画再生中かどうかの管理
        self.frame_timer = 0# フレーム進行する間隔
        self.draw_timer = 50# 描画する間隔

        self.gd_flag = gd_flag
        self.result_flag = False
        self.f_name = 'face.png'
        self.save_name = 'myFace.png'
        #self.result_name = 'result.png'
        self.result_name = 'result.mp4'
        
        self.gd_connect = GdriveConnect(self.img_path, '1LWrt1WR4DOceXUvSE6qvMcjMS8xzWlQd')


        self.bg_width = 800
        self.bg_canvas = tk.Canvas(self.frame, width=self.bg_width, height=self.pic_size)

        self.message = tk.StringVar(self.frame)
        self.message.set('Please wait ......')

        self.button_text = tk.StringVar(self.frame)
        self.button_text.set('restart')
        
        # 各種ウィジェットの作成
        self.widgets.append(tk.Label(self.frame, textvariable=self.message, font=("MSゴシック", "20"), anchor=tk.CENTER))
        self.widgets.append(tk.Button(self.frame, textvariable=self.button_text,  font=("MSゴシック", "50", "bold"), command=self._back))
        self.widgets.append(self.bg_canvas)
        
        # 各種ウィジェットの設置
        pack_modes = [0, 0, 2]
        super().draw_widget(pack_modes)

    def get_result(self):
        if self.result_flag:
            return
        
        self.result_flag = self.gd_connect.file_download(self.result_name, self.save_name)
        
        if self.result_flag:
            self.message.set("Here is the age-variant.")
            self.face_video = cv2.VideoCapture(self.img_path + self.result_name)

            self._draw_face()
        else:
            time.sleep(10)
            #self.get_result()

    def draw_result_video(self):
        if not self.result_flag:
            return

        if not self.face_video:
            return

        # フレームの読み込み
        ret, self.video_frame = self.face_video.read()
         # フレームが進められない場合
        if not ret:
            # フレームを最初に戻す
            self.face_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, self.video_frame = self.face_video.read()
        # PIL イメージに変換
        rgb_frame = cv2.cvtColor(self.video_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        
        ratio = 0.5
        # リサイズ
        self.video_image = pil_image.resize(
            (
                int(ratio * pil_image.width),
                int(ratio * pil_image.height)
            )
        )
        if self.video_image is not None:
            # Tkinter画像オブジェクトに変換
            self.video_image_tk = ImageTk.PhotoImage(self.video_image)
        self.bg_canvas.create_image(self.bg_width - self.pic_size/2, self.pic_size/2, image=self.video_image_tk)


    def _draw_face(self):
        self.org_img = ImageTk.PhotoImage(file = self.img_path + self.f_name)
        self.arr_img = ImageTk.PhotoImage(file = self.img_path + 'arrow.png')
        self.bg_canvas.create_image(self.pic_size/2, self.pic_size/2, image=self.org_img)
        self.bg_canvas.create_image(self.bg_width/2, self.pic_size/2, image=self.arr_img)

        if self.result_flag:
            self.draw_result_video()
            #self.res_img = ImageTk.PhotoImage(file = self.img_path + self.result_name)
            #self.bg_canvas.create_image(self.bg_width - self.pic_size/2, self.pic_size/2, image=self.res_img)
    
    def _back(self):
        self.result_flag = False
        self.message.set('Please wait ......')
        self.bg_canvas.delete("all")
        self.ready_mode = self.route[0]

    def raise_page(self):
        #print('raise vr')
        self._draw_face()
        super().raise_page()
        if self.gd_flag:
            self.gd_connect.file_upload(self.f_name, self.save_name, [self.result_name])

