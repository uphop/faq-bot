# faq-bot

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

sudo chmod 666 /var/run/docker.sock

change pwd:
sudo su -
passwd ubuntu

sudo groupadd docker
sudo usermod -aG docker $USER

Start: 
docker-compose up -d
./ngrok start --config ngrok.yml rasa

Stop: 
docker-compose down --volumes --remove-orphans
