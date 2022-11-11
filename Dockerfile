# базовый образ
FROM debian:bullseye-slim

# установка рабочей директории (по умолчанию) в образе и переменной для директории проекта
WORKDIR /app
ARG project_path=./convert2pdf

# установка необходимого ПО
RUN set -ex ;\
    apt-get update ;\
    apt-get install -y --no-install-recommends python3-pip libgl1 openjdk-11-jre unoconv fonts-nanum \
    libreoffice-calc libreoffice-writer libreoffice-java-common wkhtmltopdf;\
    apt-get clean && rm -rf /var/lib/apt/lists/* ;\
    touch TOKEN.env

# копирование файла зависимостей
COPY $project_path/requirements.txt .

# установка зависимостей через pip
RUN pip3 install -r requirements.txt

# копирование проекта в образ
COPY $project_path/*.py ./

# установка макроса (для конвертера xls-файлов)
RUN soffice --headless --nologo --nofirststartwizard --norestore 1.xlsx macro:///Standard.Module1.FitToPage
RUN rm -f /root/.config/libreoffice/4/user/basic/Standard/Module1.xba
COPY $project_path/*.xba /root/.config/libreoffice/4/user/basic/Standard/

# запуск скрипта при запуске контейнера
ENTRYPOINT ["python3", "main.py"]