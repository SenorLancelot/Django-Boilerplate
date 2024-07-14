FROM python:3.8 as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /home/backend
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt 

COPY . .
RUN chmod -R 777 .

# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0:8000", "--noreload", "--insecure"]
