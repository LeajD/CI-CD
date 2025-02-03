FROM ubuntu:20.04
LABEL version="0.1"

# Install apache2, python3 and python3 pip
ENV TZ=Europe/Warsaw 
RUN apt-get update \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get install -y -qq \
        python3.8 \
        python3.8-dev \
        python3.8-distutils \
        apt-utils \
        curl \
    && apt-get install -y \
        apache2 \
        apache2-utils \
        libssl1.0 \
        software-properties-common \
        mc \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y \
        libapache2-mod-wsgi-py3 \
        pgbouncer \
    && rm -rf /var/lib/apt/lists/*  \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.8 get-pip.py

# RUN pip3 install pillow==8.3
RUN python3.8 -m pip install pillow==8.3 \
        Cython \
        elasticsearch

# Upgrade pip and install python packages
RUN python3.8 -m pip install django \
        pip \
        python-pptx \
        pytz \
        ipaddress \
        apscheduler \
        requests \
        python-docx \
        si-prefix  \
        tzdata \
        matplotlib \
        asgiref 

RUN update-rc.d pgbouncer defaults \
    && echo '"django" "django"' > /etc/pgbouncer/userlist.txt \
    && service pgbouncer start \
    && a2enmod rewrite \
    && a2enmod ssl

# Copy website config
ADD ./config/demo_site.conf /etc/apache2/sites-available/000-default.conf

# Make directory and copy project there
RUN mkdir -p /var/www/django
COPY [--chown=www-data:www-data] . /var/www/django

# Some env values stuff
ARG POSTGRES_DB=None
ENV POSTGRES_DB=$POSTGRES_DB

ARG POSTGRES_HOST=None
ENV POSTGRES_HOST=$POSTGRES_HOST

ARG POSTGRES_PASSWORD=None
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD

ARG POSTGRES_PORT=None
ENV POSTGRES_PORT=$POSTGRES_PORT

ARG POSTGRES_USER=None
ENV POSTGRES_USER=$POSTGRES_USER



ARG POSTGRES_USER=None
ENV POSTGRES_USER=$POSTGRES_USER

EXPOSE 80


RUN /sbin/apache2ctl start

ENTRYPOINT ["apache2ctl", "-D", "FOREGROUND"]
