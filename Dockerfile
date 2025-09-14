FROM python:3.10

WORKDIR /app

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    pdf2svg \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY *.py ./
COPY endpoint endpoint/
COPY pdf pdf/
COPY test test/

CMD ["uvicorn", "main:app", "--proxy-headers", "--root-path", "/api/v1", "--host", "0.0.0.0", "--port", "8000"]
