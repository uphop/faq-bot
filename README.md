# faq-bot

## About
<TBD>

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
`docker-compose up -d`

Also, if you are running on a local machine, you need to start a public channel:
`./ngrok start --config ngrok.yml rasa`

After several seconds all containers should be started, and Capture Bot should be listening on the channel exposed to Slack.
Try that out now, by openning Slack workspace where you have configured the bot app, and sayind "Hi" :)

### Stop
To stop, ask Docker Compose to ramp own all launched containers:
`docker-compose down`

And to fully clean-up, you can run the following:
`docker-compose down --volumes --remove-orphans --rmi all`

## Additional configuration and deployment optons

### Enable GPU support

You can leverage GPU support to train new FAQ bots much quicker. For that:
* Set-up Nvidia drivers as per [this guide](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html#introduction)
* Set-up CUDA Tookit as per [this guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#introduction)
* Uncomment GPU configuration in `docker-compose.yml`, service `publish-broker`

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
`sudo chmod 666 /var/run/docker.sock`

Also, if you are running locally on Mac, you need to talk to `docker.sock.raw` instead of `docker.sock`. Please modify volume config in `docker-compose.yml`, service `publish-broker` as per comments in that section. For more details, check [this thread](https://github.com/docker/for-mac/issues/4755).

### "Permission denied" while trying to access host Docker daemon

You may need to add your user to the Docker group:
`sudo groupadd docker`
`sudo usermod -aG docker $USER`

Please see the [following thread](https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket) for more details.

Also, check whith which user you are running containers. You may need to run as root:
`sudo docker-compose up -d`





