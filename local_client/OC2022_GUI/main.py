# -*- coding: utf-8 -*-
#This is Prototype StyleCariGAN-GUI code.

import tkinter as tk
import argparse

from home import Home
from confirm_face import ConfirmFace
from view_result import ViewResult

root = None
pages = []
now_page = -1

def update_page():
    global root, pages, now_page

    if now_page == 0:
        pages[0].show_cam()
        pages[0].draw_update()
    if now_page == 2:
        pages[2].get_result()
        pages[2]. draw_result_video()

    trans = pages[now_page].get_status()

    if not trans == -1:
        pages[now_page].reset_page()
        now_page = trans
        pages[now_page].raise_page()

    root.after(100, update_page)

def main():
    global root, pages, now_page

    img_path = './imgs/'
    root = tk.Tk()
    root.title("StyleGAN-GUI")
    root.geometry("1000x600")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # まずオブジェクト生成
    parser = argparse.ArgumentParser()
    # 引数設定
    parser.add_argument("--internal", action="store_false")
    args = parser.parse_args()
    # 参照できる
    #args.param

    pages.append(Home(root, [0, 1], img_path, 450))
    pages.append(ConfirmFace(root, [0, 2], img_path, 300))
    pages.append(ViewResult(root, [0], img_path, 300, args.internal))

    now_page = 0
    pages[0].raise_page()
    update_page()

    root.mainloop()

if __name__ == '__main__':
    main()
    