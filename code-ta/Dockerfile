FROM python:3.10

EXPOSE 8080

WORKDIR /code_tester

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"] 

CMD ["manage.py", "runserver", "0.0.0.0:8080"]