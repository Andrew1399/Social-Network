FROM python:3.9.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . code
WORKDIR /social_network

RUN pip install --upgrade pip

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
