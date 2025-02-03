FROM python:3.9
USER root
RUN apt-get update && apt-get install -y openssl libc-bin libc-dev-bin libc6 libc6-dev libglib2.0-* linux-libc-dev 

WORKDIR /app

RUN useradd -m -s /bin/bash pyappuser
COPY tls-checker.py /app/tls-checker.py
COPY start.sh /app/start.sh
COPY send-webhook.sh /app/send-webhook.sh
COPY tls-domains /app/tls-domains
RUN chown -R pyappuser:pyappuser /app

RUN pip3.9 install --upgrade pip
RUN pip3.9 install setuptools

USER pyappuser

CMD ["bash", "/app/start.sh"]