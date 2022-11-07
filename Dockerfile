# базовый образ
FROM debian:bullseye-slim
# установка рабочей директории (по умолчанию) в образе
WORKDIR /app
ARG project_path=./convert2pdf
# ставим unoconv
RUN set -ex ;\
    apt-get update ;\
    apt-get install -y --no-install-recommends python3-pip libgl1 openjdk-11-jre unoconv fonts-nanum \
    libreoffice-calc libreoffice-writer libreoffice-java-common wkhtmltopdf;\
    # apt-get install -y --no-install-recommends python3-pip libgl1 openjdk-11-jre unoconv libreoffice-calc libreoffice-writer;\
    # apt-get install -y  fonts-nanum;\
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    touch TOKEN.env
# копирование файла зависимостей
COPY $project_path/requirements.txt .
# установка зависимостей через pip
RUN pip3 install -r requirements.txt
# копирование скриптов
COPY $project_path/*.py ./

# Change macros file
RUN soffice --headless --nologo --nofirststartwizard --norestore 1.xlsx macro:///Standard.Module1.FitToPage
RUN rm -f /root/.config/libreoffice/4/user/basic/Standard/Module1.xba
COPY $project_path/*.xba /root/.config/libreoffice/4/user/basic/Standard/

# COPY TOKEN.env ./
# запуск скрипта при запуске контейнера
ENTRYPOINT ["python3", "main.py"]