# Backup Engine

A python module easy to do local backup and google cloud backup for Flask web application.



## Requirements

> Environment：Python 3

* pymongo
* google-api-python-client
* google-auth-httplib2
* google-auth-oauthlib



## API

###dbClinet - Tools for connect to database and then can easy to do local backup

####class `backup_engine.dbClient.Connect(db=None, client=None, host=None, port=None)`

> Client object which is connecting to the database

* **Parameters**

  * db (str)：which database type you want to backup. Now just support `mongo`
  * client (db client obj)：the instance of db's client
  * host (str)：host or ip address
  * port (str)：db's port

* **Functions**

  **local_backup()**：Do local backup from database, it will export and dackup all table of specific database.

  * Parameters

    * **db_name**: the name of the database which you want to backup

    * **dir_path**: the location where you want to save your backup folders. Default: BASE_DIR/backup
    * **dir_name**: the name of the folder in this time backup, the folder will save your this time     backup files

    * **table_name**: if has value means don't want to backup all table, just the specific table

    

## Examples

#### local backup

If alreay have the instance of the database client object

~~~python
import pymongo
from backup_engine import dbClient

MONGO_URI = 'your mongodb URI'
client = pymongo.MongoClient(MONGO_URI, connect=False)
backup_client = dbClient.Connect(db='mongo', client=client)
backup_client.local_backup('db_name')
~~~

If not, you can do this

~~~python
from backup_engine import dbClient

backup_client = dbClient.Connect(db='mongo', host='your_db_host', port='27017')
backup_client.local_backup('db_name')
~~~



## License

2019, Ching-Hsuan Su

MIT