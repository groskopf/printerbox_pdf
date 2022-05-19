FROM python:3.10

WORKDIR /app

# TODO add user

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY *.py ./
COPY endpoint endpoint/
COPY pdf pdf/
COPY test test/

CMD ["uvicorn", "main:app", "--proxy-headers", "--root-path", "/api/v1", "--host", "0.0.0.0", "--port", "8000"]
