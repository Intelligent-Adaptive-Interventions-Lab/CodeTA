FROM python:3.10-alpine3.17

WORKDIR /code_ta/python_exec

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./script.py ./

CMD [ "python3", "script.py" ]