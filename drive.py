import os
import pickle
import os
from datetime import datetime
import time
import logging
from os import listdir
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload


class Drive:
    '''Google Drive's instance that upload the backup folder to google drive
        - auth_path: the folder path where have token.pickle and credentials.json file
    '''

    BASE_DIR = os.getcwd()
    AUTH_PATH = os.path.join(os.getcwd(), 'auth')

    def __init__(self, auth_path=None):
        if auth_path == None:
            auth_path = self.AUTH_PATH

        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(auth_path, 'token.pickle')):
            with open(os.path.join(auth_path, 'token.pickle'), 'rb') as token:
                creds = pickle.load(token)
                print('已經取得creds認證')
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('未取得權限, 請登入google drive')
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(os.path.join(auth_path, 'credentials.json'), SCOPES)
                    creds = flow.run_local_server()
                except:
                    print('找不到 credentials.json 此檔案')
            
            # Save the credentials for the next run
            with open(os.path.join(auth_path, 'token.pickle'), 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def backup(self, local_backup_path=None, drive_folder_id=None, drive_folder_name=None, log=False):
        '''Choose specific dir and upload to your
            Parameters:
                - local_backup_path: the folder path which in local you want to upload to google drive.
                    default: [BASE_DIR]/backup/[todayDate]
                - drive_folder_id: the id of your google drive folder
                - drive_folder_name: the name of the folder in this time backup, the folder will save your upload   from local
                    default: [todayDate]
                - log: if True, then backup log files
        '''

        todayDate = datetime.now().strftime("%Y-%m-%d") # today's date
        LOCAL_BACKUP_PATH = os.path.join(self.BASE_DIR, "backup", todayDate)
        LOG_PATH = os.path.join(self.BASE_DIR, "logs")
        
        if local_backup_path == None:
            local_backup_path = LOCAL_BACKUP_PATH
        if drive_folder_id == None:
            raise TypeError('must need google drive folder id')
        if drive_folder_name == None:
            drive_folder_name = todayDate

        log_path = ''
        if log == True:
            log_path = LOG_PATH


        # create folder
        BACKUP_FOLDER_ID = drive_folder_id # 認知訓練之臨床應用>backup
        folder_metadata = {
            'name': drive_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [BACKUP_FOLDER_ID]
        }
        folder = self.service.files().create(body=folder_metadata,
                                             fields='id').execute()
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"), '成功在google drive創建資料夾')
        FOLDER_ID = folder.get('id') # 當下創建的folder id

        # 本地backup資料夾內的檔案
        files = listdir(local_backup_path)
        for f in files:
            fullpath = os.path.join(local_backup_path, f)

            # 檢查文件大小，除果0kb就不上傳
            fileSize = os.path.getsize(fullpath)
            if (fileSize>0):
                file_metadata = {
                    'name' : f,
                    'parents': [FOLDER_ID]
                }
                media = MediaFileUpload(fullpath,
                                        resumable=True)
                file = self.service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
                print('成功上傳', f, '到雲端')


        ### 備份 logs ###
        if log == True:
            log_files = listdir(log_path)
            for f in log_files:
                fullpath = os.path.join(log_path, f)

                # 檢查文件大小，除果0kb就不上傳
                fileSize = os.path.getsize(fullpath)
                if (fileSize>0):
                    file_metadata = {
                        'name' : f,
                        'parents': [FOLDER_ID]
                    }
                    media = MediaFileUpload(fullpath,
                                            resumable=True)
                    file = self.service.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields='id').execute()
                    print('成功上傳', f, '到雲端')
