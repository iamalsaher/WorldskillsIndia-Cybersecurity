FROM python:3.8-slim
ENV DEBIAN_FRONTEND noninteractive
ENV BIND 0.0.0.0:8000
RUN apt update && apt -y install --no-install-recommends gcc libmariadb-dev && apt clean
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN mv /app/start.sh . && chmod +x start.sh && rm requirements.txt
ENTRYPOINT /start.sh
