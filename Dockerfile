FROM python:3.9

RUN pip install -r requirements.txt

WORKDIR /app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./printerbox_pdf /app/printerbox_pdf

CMD ["uvicorn", "printerbox_pdf.main:app", "--host", "0.0.0.0", "--port", "80"]
