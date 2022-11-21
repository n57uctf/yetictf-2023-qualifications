from fastapi import FastAPI,Request, Form, Cookie, File, UploadFile
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse,HTMLResponse,RedirectResponse, Response
from hashlib import md5
from app.secure import *
from app.sqldb import *
import starlette.status as status
import datetime
from app.models import *
import time
import uvicorn
import tempfile
import os
from io import BytesIO
from zipfile import ZipFile, ZIP_STORED

time.sleep(2)
db = SQLDB({
            'host': 'db',
            'port': '5432',
            'database': 'postgres',
            'user': 'postgres',
            'password': 'qweasdzxc1'
        })
# creating bd
db.execute('create_db').none()

# creating default user admin with password
if db.execute('read_user', {'user': 'admin'}).one() is None:
    db.execute('create_user', {'login': 'admin', 'password': hash_sha256('changeme1')}).none()

#reading an archieve in binary format
data = BytesIO()
with ZipFile(data, mode='w', compression=ZIP_STORED) as arhive:
    arhive.writestr('flag.txt', os.environ['FLAG'])
    arhive.setpassword(b'hallowen')
#print(data.getvalue()) - chisto posmotret che tam est

#uploading archieve
if db.execute('read_user_files', {'user': "1"}).all() is None:
    db.execute('upload_file', {'owner_': '1', 'name': 'flag.zip', 'content': encrypt_file_AES(data.getvalue(), 'changeme1'),'size': len(data.getvalue()),'create_date': datetime.datetime.now()}).none()
data.close()

app = FastAPI()
from app.routes import *
