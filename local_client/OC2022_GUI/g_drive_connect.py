from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import os

class GdriveConnect:
    def __init__(self, img_path, drive_folder_id):
        self.img_path = img_path
        self.drive_folder_id = drive_folder_id # 1LWrt1WR4DOceXUvSE6qvMcjMS8xzWlQd
        #Googleサービスを認証
        self.gauth = GoogleAuth()

        #資格情報ロードするか、存在しない場合は空の資格情報を作成
        self.gauth.LoadCredentialsFile("mycreds.txt")
        
        if self.gauth.credentials is None: #Googleサービスの資格情報がない場合
            self.gauth.LocalWebserverAuth()#ユーザーから認証コードを自動的に受信しローカルWebサーバーを設定

        elif self.gauth.access_token_expired:#アクセストークンが存在しないか、期限切れかの場合
            self.gauth.Refresh()#Googleサービスを認証をリフレッシュする

        else:#どちらにも一致しない場合
            self.gauth.Authorize()#Googleサービスを承認する

        #資格情報をtxt形式でファイルに保存する  
        self.gauth.SaveCredentialsFile("mycreds.txt") 
            
        #Googleドライブの認証処理
        self.drive = GoogleDrive(self.gauth)

    def file_upload(self, f_name, save_name, del_names):
        #f_name = 'myFace.png'などを保存時の名前を指定

        #入力画像の消去
        file_exists = self.drive.ListFile({'q': 'title = "{}" and "{}" in parents'.format(save_name, self.drive_folder_id)}).GetList()
        if len(file_exists) > 0:
            file_id = file_exists[0]['id']
            rm_f = self.drive.CreateFile({'id': file_id})
            rm_f.Delete()

        #結果画像の消去
        if len(del_names) > 0:
            for del_name in del_names:
                file_exists = self.drive.ListFile({'q': 'title = "{}" and "{}" in parents'.format(del_name, self.drive_folder_id)}).GetList()
                if len(file_exists) > 0:
                    file_id = file_exists[0]['id']
                    rm_f = self.drive.CreateFile({'id': file_id})
                    rm_f.Delete()

        f = self.drive.CreateFile({'title' : save_name, 'parents' : [{'id' : self.drive_folder_id}]})
        
        f.SetContentFile(self.img_path + f_name)#ローカルのファイルをセットしてアップロード
        f.Upload()#Googleドライブにアップロード
        f = None
    
    def file_download(self, result_name, save_name):
        file_exists = self.drive.ListFile({'q': 'title = "{}" and "{}" in parents'.format(result_name, self.drive_folder_id)}).GetList()
        if len(file_exists) > 0:
            file_id = file_exists[0]['id']
            f = self.drive.CreateFile({'id': file_id})
            f.GetContentFile(self.img_path + result_name)
            f.Delete()
            return True
        else:
            return False
            