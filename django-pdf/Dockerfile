FROM python:3.8

RUN useradd demo

WORKDIR /home/demo
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements.txt requirements.txt

COPY . .
#RUN pip install /home/demo/

RUN chown -R demo:demo /home/demo
USER demo

ENV DJANGO_SETTINGS_MODULE=django_pdf.settings_dev
ENV UWSGI_WSGI_FILE=django_pdf/wsgi.py
ENV UWSGI_HTTP=0.0.0.0:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy
# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=1 UWSGI_THREADS=4

EXPOSE 8000
#CMD python manage.py runserver
CMD ["uwsgi", "--show-config", "--static-map", "/static=/home/demo/static"]