"""Tools for connect to database and then can easy to do local backup.
"""

import os
import time
import json
from datetime import datetime
from bson import json_util

class Connect:
    '''Client object which is connecting to the database
        Parameters:
            - db: mongo
            - client: the instance of db's client
            - host: host or ip address
            - port: db's port
    '''

    BASE_DIR = os.getcwd()
    
    HOST = "localhost"
    MONGO_PORT = 27017

    def __init__(self, db=None, client=None, host=None, port=None):
        if db == None:
            raise TypeError("db must choose one, now just support mongo")
        else:
            self._db = db
        
        if client == None:
            if host == None:
                host = self.HOST
            if port == None:
                if db == 'mongo':
                    port = self.MONGO_PORT

        # if all already
        if db == 'mongo':
            try:
                import pymongo
            except:
                raise EnvironmentError("need install 'pip install pymongo'")

            if client:
                self._client = client
            else:
                self._client = pymongo.MongoClient(host=host, port=port)
        
    
    def local_backup(self, db_name=None, dir_path=None, dir_name=None, table_name=[]):
        '''Do local backup from database, it will export and dackup all table of specific database.
            Parameters:
                - db_name: the name of the database which you want to backup
                - dir_path: the location where you want to save your backup folders.
                    default: BASE_DIR/backup
                - dir_name: the name of the folder in this time backup, the folder will save your this time         backup files
                - table_name: if has value means don't want to backup all table, just the specific table
        '''

        if db_name == None:
            raise TypeError("need db name")
        if dir_path == None:
            dir_path = os.path.join(self.BASE_DIR, 'backup')
        if dir_name == None:
            todayDate = datetime.now().strftime("%Y-%m-%d") # today's date
            dir_name = todayDate
        
        # check whether is the backup folder exist
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
            print(dir_path, 'not exist!', 'create', dir_path, 'success')

         # the path of this time backup
        local_backup_path = os.path.join(dir_path, dir_name)

        # create the folder of this time backup
        try:
            # mkdir_cmd = 'mkdir ./backup/' + nowTime # in linux
            # mkdir_cmd = 'mkdir .\\backup\\' + nowTime # in win
            mkdir_cmd = 'mkdir ' + local_backup_path
            os.system(mkdir_cmd)
            print('create', dir_name, 'folder success')
        except Exception as err:
            print('create', dir_name, 'folder fail')
            print('err:', err)
        

        # backup all collections
        if self._db == 'mongo':
            db = self._client[db_name]
            collections_name = db.collection_names()

            for col_name in collections_name:
                col = db[col_name]
                cursor = col.find({})

                file = open(local_backup_path+'/'+col_name+'.json', "w", encoding='utf-8')
                for document in cursor:
                    file.write(json.dumps(document, default=json_util.default, ensure_ascii=False))
                    file.write('\n')
                    
                print('complete backup', col_name, 'at', time.strftime("%A, %d. %B %Y %I:%M:%S %p"))