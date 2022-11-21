FROM python:3.10

#
WORKDIR /code
#
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app
COPY ./sql /code/sql
COPY ./templates /code/templates

#
CMD ["uvicorn","app.main:app","--reload", "--host", "0.0.0.0" ,"--port","15400"]
