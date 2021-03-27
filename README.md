# faq-bot

## About
<TBD>

## Setting-up

### Install pre-requisites

The project is packaged as 4 custom-built Docker containers, plus Postgres and RabbitMQ. You need to the following to start-up:
* [Docker runtime](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

All other dependencies should be handled during container build.

### Init environment config

Environment variables of each project are kept in the project's `.env` file:
* `faq-capture-actions/.env` - configuration of Rasa action server for Capture Bot
* `faq-publish-api/.env` - configuration of Flask app for Publish API
* `faq-publish-broker/.env` - configuration of Celery broker for Publish API

Please init those by running `./init_config.sh`, which will copy sample configuration, and then  and modify `.env` files in each project if needed. 

### Configure Slack integration

Please configure Rasa<>Slack integration for Capture Bot as per [this guide](https://rasa.com/docs/rasa/connectors/slack/).

You will need to update two config files:
* In `faq-capture-bot/credentials.yml`, set values of `slack_token` to your Slack token, and `slack_signing_secret` to your Slack secret
* In `faq-capture-actions/.env`, set value of `SLACK_BOT_TOKEN` to your Slack token

### Environment

### Running

Start: 
docker-compose up -d
./ngrok start --config ngrok.yml rasa

Stop: 
docker-compose down --volumes --remove-orphans --rmi all

### GPU support
Set-up Nvidia drivers
GPU set-up:
https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#post-installation-actions
https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html#ubuntu-lts

### Deploying to AWS








Troubleshooting:

Prep:
change Docker for Mac settings, increase memory limit to 4GB, swap to 2GB
Slack config
.env config

HTTPS:
https://datahive.ai/deploying-rasa-chatbot-on-google-cloud-with-docker/

AWS:
https://www.twilio.com/blog/deploy-flask-python-app-aws 

Install Docker:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04

Change permissions and add user to acess host daemon:
sudo chmod 666 /var/run/docker.sock
sudo groupadd docker
sudo usermod -aG docker $USER

change pwd:
sudo su -
passwd ubuntu





