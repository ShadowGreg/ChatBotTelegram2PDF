# базовый образ
FROM debian:bullseye-slim
# установка рабочей директории (по умолчанию) в образе
WORKDIR /app
# ставим unoconv
RUN set -ex ;\
    apt-get update ;\
    apt-get install -y --no-install-recommends python3-pip unoconv libreoffice-calc;\
    apt-get install -y  fonts-nanum;\
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    touch TOKEN
# копирование файла зависимостей
COPY req.txt .
# установка зависимостей через pip
RUN pip3 install -r req.txt
# копирование скриптов
COPY *.py ./
COPY TOKEN ./
# запуск скрипта при запуске контейнера
CMD ["python3", "main.py"]