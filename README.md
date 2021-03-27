# FAQ assistant with Rasa

## About

### Purpose

This project is a Slack-based assistant, which miitgates [Slacktique](https://www.reddit.com/r/Slack/comments/ho5uq7/slacktigue_what_are_your_tips_and_tricks/) by acting as your personal proxy between people asking you recurring, similar questions over Slack, and yourself. 

The primary use case is the following:
* Capture some specific knowledge from the individual what individual's peers most probably will be asking multiple times, and the individual would like to share once with all (e.g. status of your specific tasks, details of your current progress, your vacation plans, etc.)
* Publish those details as a personalized bot, which is proxying all FAQ requests, and allow anyone to pull those details asynchronously 
* You can feed-in new details at any time, a new bot is retrained in background, and updated details are published to your peers in a couple of minutes

There are two bot types:
* A concierge bot (Capture) is launched for all users, collects frequently asked questions / answers (FAQs) from each user, and then dynamically generates training data, trains and launches a dedicated bot for that user to serve those FAQs
* A dedicated bot (Broadcast) is launched per each user, and serves published FAQs to other people, who are talking to the bot instead of you

### Usage and demo

Open a Slack direct message channel with the bot app: Apps > Add apps > (find your bot app and select that)

Say "Hi" :) the bot should respond with the following:
![Screenshot 2021-03-27 at 12 52 56](https://user-images.githubusercontent.com/74451637/112718407-6c4f3d80-8efb-11eb-98ac-98f62599ceeb.png)

### Implementation

The project consists of the following modules:
* Concierge bot (Capture) in `faq-capture-bot`: this is a master bot which collects FAQs and publishes those to `faq-publish-api`. The bot is implemented with [Rasa Open Source](https://rasa.com/docs/rasa/).
* Concierge bot's action server in `faq-capture-actions`: this is an add-on service supporting Concierge bot with custom logic. Action server is using Pubslish API to pass FAQs for publishing. Also, Aciton server dynamically calls published Broadcast bots via Rasa REST API. The server is implemented with [Rasa Action Server](https://rasa.com/docs/action-server).
* Publish API in `faq-publish-api`: this is a RESTful API to manage users and their FAQs. API is implemented with Flask, SQLAlchemy and Postgres. Also, that talks to Publish Broker via RabbitMQ queue to send pubslih tasks.
* Publish Broker in `faq-publish-broker`: this is a Celery worker, which generates new Rasa bots with to servce FAQs, and runs those as dedicated Docker containers. Broker is implemented with [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html).

## Setting-up

### Install pre-requisites

The project is packaged as 4 custom-built Docker containers, plus Postgres and RabbitMQ. You need the following to start-up:
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

Also, you will need to create a new bot app in Slack for Capture Bot, and to configure Rasa<>Slack integration as per [this guide](https://rasa.com/docs/rasa/connectors/slack/).

You will need to update two config files:
* In `faq-capture-bot/credentials.yml`, set values of `slack_token` to your Slack token, and `slack_signing_secret` to your Slack secret
* In `faq-capture-actions/.env`, set value of `SLACK_BOT_TOKEN` to your Slack token

If you are going to run on a local machine, you may need to open a channel visible to Slack, for example with [ngrok](https://ngrok.com/).
A sample ngrok configuration is provided in `ngrok.yml`.

## Starting-up

### Start
To start, launch Docker Compose build: 
```
docker-compose up -d
```

Also, if you are running on a local machine, you need to start a public channel: 
```
./ngrok start --config ngrok.yml rasa
```

After several seconds all containers should be started, and Capture Bot should be listening on the channel exposed to Slack.
Try that out now, by openning Slack workspace where you have configured the bot app, and saying "Hi" :)

### Stop
To stop, ask Docker Compose to ramp own all launched containers: 
```
docker-compose down
```

And to fully clean-up, you can run the following: 
```
docker-compose down --volumes --remove-orphans --rmi all
```

## Additional configuration and deployment optons

### Enable GPU support

You can leverage GPU support to train new FAQ bots much quicker. For that:
* Set-up Nvidia drivers as per [this guide](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html#introduction)
* Set-up CUDA Tookit as per [this guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#introduction)
* Uncomment GPU configuration in `docker-compose.yml`, service `publish-broker`
```
  publish-broker:
    ...
    environment:
      NVIDIA_VISIBLE_DEVICES: all
      NVIDIA_DRIVER_CAPABILITIES: all
    deploy:
      resources:
        reservations:
          devices:
          - capabilities: [gpu]
    ...
```

### Deploy to AWS

I have tried deploying this project to a single EC2 instance on AWS, on t2.xlarge (general purpose instance, without GPU) and g4.dn.xlarge (general purpose instance, with GPU). 
The project is mostly compute-hungry, and a bit less memory-hungry (with the current configuration, each Rasa bot retraining takes up to 1-x cores, and ~1GB).
Therefore, recommended minimum configuration is 4x vCPUs / 1x GPU (if available), and 8GB memory.

You will need to also configure HTTPS support and reverse proxy in order to expose the Capture Bot to Slack. Please check [this](https://blog.cloudboost.io/setting-up-an-https-sever-with-node-amazon-ec2-nginx-and-lets-encrypt-46f869159469) and [this](https://jay315.medium.com/installing-ssl-tls-certificates-on-aws-ec2-with-ubuntu-and-nginx-configuration-eb156a55f7e7) amazing guides.

## Troubleshooting

### "Killed" message while training Rasa bot on MacOS

If you are running on Mac, please note that Docker for Mac has rather low limits by default. Please refer to this [guide](https://docs.docker.com/docker-for-mac/) for details how to configure those.
You may need to increase memory limit to 4GB, and memory swap to 2GB to run locally.

### Cannot access host Docker socket

You may need to grant permissions to access Docker socket:
```
sudo chmod 666 /var/run/docker.sock
```

Also, if you are running locally on Mac, you need to talk to `docker.sock.raw` instead of `docker.sock`. Please modify volume config in `docker-compose.yml`, service `publish-broker` as per comments in that section. 
```
 publish-broker:
    ...
    volumes: 
      # Please note Docker for Mac requires the following
      # - /var/run/docker.sock.raw:/var/run/docker.sock'
      # However, on other Linux (e.g. AWS EC2 Ubuntu) change to:
      # - /var/run/docker.sock:/var/run/docker.sock'
      # See for details: https://github.com/docker/for-mac/issues/4755
      - /var/run/docker.sock.raw:/var/run/docker.sock
    ...
```

For more details, check [this thread](https://github.com/docker/for-mac/issues/4755).

### "Permission denied" while trying to access host Docker daemon

You may need to add your user to the Docker group:
```
sudo groupadd docker
sudo usermod -aG docker $USER
```

Please see the [following thread](https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket) for more details.

Also, check whith which user you are running containers. You may need to run as root:
```
sudo docker-compose up -d
```





