from app.main import *

templates = Jinja2Templates(directory="./templates/")

@app.get("/")
async def get_disk(request: Request, laset: str | None = Cookie(default=None)):
    if laset is None:
        return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
    else:
        result = db.execute('read_user', {'user': verify_auth_token(laset)}).one(User)
        result1 = db.execute('read_user', {'user': verify_auth_token(laset)}).one()
        massiv = db.execute('read_user_files', {'user': result.user_id}).all()
        #print(massiv)
        return templates.TemplateResponse('./disk.html', context={'request': request, 'username': result.username,
                                                                  'emd6': result.password, 'massiv': massiv})

@app.get("/login", response_class=HTMLResponse)
def get_login(request: Request, response : Response):
    response = templates.TemplateResponse('./login.html',context={'request': request})
    response.delete_cookie(key='laset', domain='127.0.0.1')
    return response

@app.post("/login")
async def post_login(request: Request, response: Response, log: str = Form(...), passwd: str = Form(...)):
    print(f'login: {log}')
    print(f'password: {hash_sha256(passwd)}')
    result = db.execute('read_user', {'user': log}).one(User)
    if (result == None):
        return RedirectResponse('/register', status_code=status.HTTP_302_FOUND)
    elif verify_hash(result.password, passwd):
        print('Success!')
        response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
        response.set_cookie(key='laset', value=get_auth_token(log), domain='127.0.0.1')
        return response
    else:
        return templates.TemplateResponse('./login.html', context={'request': request, 'emd6': 'Password incorrect!'})


@app.get("/register")
async def get_register(request: Request):
    return templates.TemplateResponse('./register.html', context={'request': request})


@app.post("/register", response_class=RedirectResponse)
async def post_register(request: Request, reg: str = Form(...), passwd1: str = Form(...), passwd2: str = Form(...)):
    print(f'login: {reg}')
    result = db.execute('read_user', {'user': reg}).one()
    if hash_sha256(passwd1) == hash_sha256(passwd2) and result is None:
        print(f'password: {hash_sha256(passwd1)}')
        print(f'password: {hash_sha256(passwd2)}')
        db.execute('create_user', {'login': reg, 'password': hash_sha256(passwd1)}).none()
        print(get_auth_token(reg))
        # return templates.TemplateResponse('register.html',context={'request': request})
        # return RedirectResponse('/')
        # return templates.TemplateResponse('./login.html', context={'request':request})
        return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
    elif result is not None:
        return templates.TemplateResponse('register.html',
                                          context={'request': request, 'invalpass': "That username is already taken!"})
    else:
        return templates.TemplateResponse('register.html',
                                          context={'request': request, 'invalpass': "Passwords aren't similar!"})


@app.get("/file")
async def get_download(passw : str,id : int, request: Request, laset: str | None = Cookie(default=None)):
    #print(id)
    risalt = db.execute('read_file_id',{'files_id' : id}).one(FileDownload)
    #print(risalt.content.tobytes())
    result = db.execute('read_user', {'user': verify_auth_token(laset)}).one(User)
    massiv = db.execute('read_user_files', {'user': result.user_id}).all()
    #print(massiv)
    if(verify_hash(result.password, passw)):
        with tempfile.NamedTemporaryFile(mode="w+b", suffix=risalt.filename[:-4], delete=False) as FOUT:
            FOUT.write(decrypt_file_AES(risalt.content, passw))
            return FileResponse(FOUT.name, filename=risalt.filename)
    else:
        with tempfile.NamedTemporaryFile(mode="w+b", suffix=risalt.filename[:-4], delete=False) as FOUT:
            FOUT.write(risalt.content)
            return FileResponse(FOUT.name, filename=risalt.filename)


@app.post("/file")
async def post_upload(request : Request,passw : str = Form(...),bool_crypt : bool = Form(False), files: UploadFile = File(...),laset: str | None = Cookie(default=None)):
    result = db.execute('read_user', {'user': verify_auth_token(laset)}).one(User)
    res = verify_hash(result.password, passw)
    massiv = db.execute('read_user_files', {'user': result.user_id}).all()
    #print(id)
    if verify_hash(result.password, passw):
        # print(file_data)
        # print(files.filename)
        # print(len(file_data))
        # print(datetime.now())
        file_data = await files.read()
        if len(file_data) == 0: #bug with uploading empty file
            return templates.TemplateResponse('./disk.html', context={'request': request, "username": result.username,
                                                                      'emd6': result.password, 'massiv': massiv})
        if len(file_data)>=31457280:
            return templates.TemplateResponse('./disk.html', context={'request': request, "username": result.username,
                                                                      'emd6': result.password, 'invalpass' : 'File size must be < 30 MB', 'massiv': massiv})
        #print(encrypt_file_AES(file_data, passw))
        #print(decrypt_file_AES(encrypt_file_AES(file_data, passw),passw))
        db.execute('upload_file',
                   {'owner_': result.user_id, 'name': files.filename, 'content': encrypt_file_AES(file_data,passw), 'size': len(file_data),
                    'create_date':  datetime.datetime.now() + datetime.timedelta(hours=3)}).none()
        massiv = db.execute('read_user_files', {'user': result.user_id}).all()
        # print(massiv)
        # print(passw)
        return RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse('./disk.html', context={'request': request, "username": result.username,
                                                                  'emd6': result.password, 'massiv': massiv,
                                                                  'invalpass': 'Incorrect password'})
