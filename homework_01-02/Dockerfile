FROM python:3.10

ENV PIP_ROOT_USER_ACTION = ignore

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "assistant.py" ]