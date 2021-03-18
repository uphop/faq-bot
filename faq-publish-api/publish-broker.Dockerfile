# Extend the official Python image
FROM python:3.7.10-slim-buster

# Prepare app folder
WORKDIR /faq-publish-broker

# Change back to root user to install dependencies
USER root

# Change owner of the app folder to non-root
RUN chown -R 1001:1001 /faq-publish-broker

# Install packages from PyPI
COPY publish-broker-requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch back to non-root to run code
USER 1001

COPY . .

CMD [ "celery", "-A", "broker", "worker", "-Q", "publish_queue", "--loglevel=INFO"]