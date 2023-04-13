FROM python:3.8

# set work directory

WORKDIR /usr/src/app/

# copy project

COPY . /usr/src/app/

# install dependencies

RUN pip install --user aiogram
RUN pip install --user psycopg2
# run app

CMD ["python", "src/botik.py"]
