eval "$(pyenv init -)" && pyenv local 3.7.9
celery -A broker worker -Q publish_queue --loglevel=INFO