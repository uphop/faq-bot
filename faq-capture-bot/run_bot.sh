eval "$(pyenv init -)" && pyenv local 3.7.10
rasa run --endpoints endpoints.yml --verbose --port 5005 --enable-api --credentials credentials_local.yml