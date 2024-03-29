FROM python:3.8.3-alpine
# 
RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/
# 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#
RUN apk update
RUN apk add --no-cache \
git \
postgresql-dev \
gcc \
python3-dev \
musl-dev \
libressl-dev \
libffi-dev \
zeromq-dev \
make \
libevent-dev \
build-base
COPY . /usr/src/app/
# 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# 
ENTRYPOINT ["sh", "entrypoint.sh"]