# Extend the official Rasa SDK image
FROM rasa/rasa:2.3.4-full

# Prepare app folder
WORKDIR /faq-capture-actions

# Change back to root user to install dependencies
USER root

# Install packages from PyPI
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch back to non-root to run code
USER 1001

COPY ./actions ./actions
COPY .env .env

EXPOSE 5055 5055

# TODO: replace credentials!!!
CMD [ "run", "actions"]