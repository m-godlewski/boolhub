# base image
FROM ubuntu:20.04

# runs system update and required packages installation
RUN apt-get update && apt-get -y install cron
RUN apt-get install libpq-dev libglib2.0 -y
RUN apt-get install tcpdump libpcap0.8-dev -y
RUN apt-get install python3-pip python3.8-venv -y

# copies source code
COPY ./brainstone /code
COPY ./.env /code
WORKDIR /code

# installs python requirements
RUN pip install --no-cache-dir -r requirements.txt

# copies schedule file to the cron.d directory
COPY ./brainstone/schedule /etc/cron.d/schedule

# gives execution rights on the cron job
RUN chmod 0644 /etc/cron.d/schedule

# applies cron job
RUN crontab /etc/cron.d/schedule

# creates the log file to be able to run tail
RUN touch /var/log/cron.log

# runs the command on container startup
CMD cron && tail -f /var/log/cron.log
