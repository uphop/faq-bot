# Extend the official Rasa SDK image
FROM python:3.8-slim-buster

# Prepare app folder
WORKDIR /faq-publish-api

# Change back to root user to install dependencies
USER root

# Install packages from PyPI
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch back to non-root to run code
USER 1001

COPY . .

EXPOSE 5000 5000

CMD [ "python3", "api.py"]