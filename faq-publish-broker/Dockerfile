# Extend the official Python image
FROM rasa/rasa:2.3.4-full

# Prepare app folder
WORKDIR /faq-publish-broker

# Change back to root user to install dependencies
USER root

# Change owner of the app folder to non-root
RUN chown -R 1001:1001 /faq-publish-broker

# Install packages from PyPI
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Download Spacy model for English
RUN python3 -m spacy download en_core_web_md
RUN python3 -m spacy link en_core_web_md en --force

# Switch back to non-root to run code
USER 1001

COPY . .

ENTRYPOINT ["celery"]
CMD [ "-A", "broker", "worker", "-Q", "publish_queue", "--loglevel=INFO"]