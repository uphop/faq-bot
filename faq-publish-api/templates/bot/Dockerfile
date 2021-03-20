
FROM rasa/rasa:2.3.4-full
# Prepare app folder

WORKDIR /faq-broadcast-bot

COPY endpoints.yml endpoints.yml
COPY credentials.yml credentials.yml
COPY ./models ./models

CMD [ "run", "--endpoints" , "endpoints.yml", "--verbose", "--port", "5005", "--enable-api", "--credentials", "credentials.yml"]
