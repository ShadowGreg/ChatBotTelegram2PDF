# базовый образ
FROM debian:bullseye-slim
# установка рабочей директории (по умолчанию) в образе
WORKDIR /app
# ставим unoconv
RUN set -ex ;\
    apt-get update ;\
    apt-get install -y --no-install-recommends python3-pip libgl1 openjdk-11-jre unoconv fonts-nanum \
    libreoffice-calc libreoffice-writer libreoffice-java-common;\
    # apt-get install -y --no-install-recommends python3-pip libgl1 openjdk-11-jre unoconv libreoffice-calc libreoffice-writer;\
    # apt-get install -y  fonts-nanum;\
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    touch TOKEN.env
# копирование файла зависимостей
COPY requirements.txt .
# установка зависимостей через pip
RUN pip3 install -r requirements.txt
# копирование скриптов
COPY *.py ./
COPY *.xba ./

# Change macros file
RUN rm -f /root/.config/libreoffice/4/user/basic/Standard/Module1.xba
COPY *.xba /root/.config/libreoffice/4/user/basic/Standard/
#                /.config/libreoffice/4/user/basic/Standard
# COPY TOKEN.env ./
# запуск скрипта при запуске контейнера
ENTRYPOINT ["python3", "main.py"]