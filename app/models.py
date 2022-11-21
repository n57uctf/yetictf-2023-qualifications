from app.main import *

class User(BaseModel):
    user_id : int
    username : str
    password : str
class Files(BaseModel):
    owner_id : int
    filename : str
    size : int
    upload_date : str
class FileDownload(BaseModel):
    file_id : int
    content : memoryview
    filename : str
    class Config:
        arbitrary_types_allowed = True
