FROM python:3.8.10
COPY . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
ENV SERVER_IP=192.168.0.250
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]