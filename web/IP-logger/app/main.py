from os import environ

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jwt.exceptions import PyJWTError

from app.secure import get_auth_token, verify_auth_token, hash_sha256, verify_hash, get_random_string
from app.sqldb import SQLDB, Config

from app.logger import log

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

flag = environ['FLAG']
pg_user = environ['POSTGRES_USER']
pg_password = environ['POSTGRES_PASSWORD']
pg_database = environ['POSTGRES_DB']
pg_ipaddr = environ['POSTGRES_IPADDR']

database = SQLDB(Config(
    user=pg_user,
    password=pg_password,
    host=pg_ipaddr,
    port='5432',
    database=pg_database
))

database.execute('create_admin', None)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """
    Главная страница с кнопкой перехода на регистрацию и логин

    :param request:
    :return:
    """
    if request.cookies.get('token') is None:
        return templates.TemplateResponse("main.html", {'request': request})

    try:
        login = verify_auth_token(request.cookies.get('token'))
    except PyJWTError:
        return templates.TemplateResponse("main.html", {'request': request})

    if login == 'admin':
        return templates.TemplateResponse("home.html", {'request': request, 'flag': flag})

    report = database.execute('read_report', True, login)
    if not isinstance(report, list):
        return templates.TemplateResponse("home.html", {'request': request, 'report': []})
    report = [dict(_) for _ in report]
    for i, record in enumerate(report):
        record.update({'id': i})
    return templates.TemplateResponse("home.html", {'request': request, 'report': report})


@app.post("/", response_class=HTMLResponse)
async def new_logger(request: Request):
    """
    Главная страница с кнопкой перехода на регистрацию и логин

    :param request:
    :return:
    """
    if request.cookies.get('token') is None:
        return templates.TemplateResponse("main.html", {'request': request})

    try:
        login = verify_auth_token(request.cookies.get('token'))
    except PyJWTError:
        return templates.TemplateResponse("main.html", {'request': request})

    form_data = await request.form()
    name = form_data.get('logger_name')
    _user = database.execute('read_user', False, login)['_user']
    database.execute('create_link', False, _user, name, get_random_string())

    report = database.execute('read_report', True, login)
    if not isinstance(report, list):
        return templates.TemplateResponse("home.html", {'request': request, 'report': []})
    report = [dict(_) for _ in report]
    for i, record in enumerate(report):
        record.update({'id': i})
    return templates.TemplateResponse("home.html", {'request': request, 'report': report})


@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    """
    Логин в личный кабинет

    :param request:
    :return:
    """
    form_data = await request.form()
    login = form_data.get('login')
    password = form_data.get('password')
    result = database.execute('read_user', False, login)
    if not result:
        return RedirectResponse(request.url_for('main'), status_code=303)
    if verify_hash(result['password'], password):
        token = get_auth_token(login)
        response = RedirectResponse(request.url_for('main'), status_code=303)
        response.set_cookie('token', token)
        return response
    return templates.TemplateResponse("main.html", {'request': request})


@app.post("/register", response_class=HTMLResponse)
async def register_post(request: Request):
    """
    Регистрация на сайте

    :param request:
    :return:
    """
    form_data = await request.form()
    login = form_data.get('login')
    password = form_data.get('password')
    hash_password = hash_sha256(password)
    success = database.execute('create_user', False, login, hash_password)
    if success:
        token = get_auth_token(login)
        response = RedirectResponse(request.url_for('main'), status_code=303)
        response.set_cookie('token', token)
        return response
    return RedirectResponse(request.url_for('main'), status_code=303)


@app.get("/redirect/{intercept_link}", response_class=HTMLResponse)
async def home(request: Request, intercept_link: str):
    """
    Перехват данных о переходе и перенаправление

    :param request:
    :param intercept_link: id сгенерированной ссылки
    :return:
    """
    agent = request.headers.get('User-Agent')
    _interception = database.execute('create_interception', False, intercept_link, request.client.host)['_interception']
    with database.connection.cursor() as curs:
        query = f"UPDATE interceptions SET user_agent = '{agent}' WHERE _interception = {_interception}"
        log(f'VULNERABLE QUERY: {query}')
        try:
            curs.execute(query)
            database.connection.commit()
        except Exception:
            pass
    return RedirectResponse('http://www.google.com', status_code=303)
