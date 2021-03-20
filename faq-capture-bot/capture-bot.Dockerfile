# Extend the official Rasa SDK image
FROM rasa/rasa:2.3.4-full

# Prepare app folder
WORKDIR /faq-capture-bot

# Change back to root user to install dependencies
USER root

# Install packages from PyPI
COPY capture-bot-requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch back to non-root to run code
USER 1001

COPY endpoints.yml endpoints.yml
# TODO: replace credentials!!!
COPY credentials_local.yml credentials.yml
COPY ./models ./models

EXPOSE 5005 5005

CMD [ "run", "--endpoints" , "endpoints.yml", "--verbose", "--port", "5005", "--enable-api", "--credentials", "credentials.yml"]