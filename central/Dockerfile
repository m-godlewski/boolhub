FROM python:3.8.10
COPY . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements_central.txt
ENV SERVER_IP=192.168.0.171
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]