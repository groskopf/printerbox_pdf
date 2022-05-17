FROM python:3.9

WORKDIR /app

# TODO add user

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY endpoint endpoint/
COPY *.py ./
COPY pdf pdf/
COPY test test/

VOLUME /app/images
VOLUME /app/printer_queue

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
