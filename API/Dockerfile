FROM python:3.11.1

COPY . /

RUN pip install -r requirements.txt

#CMD uvicorn main:app --host 0.0.0.0 --port 8000

RUN chmod +x /start_api.sh

ENTRYPOINT ["/start_api.sh"]

