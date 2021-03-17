eval "$(pyenv init -)" && pyenv local 3.7.10
python3 -m unittest discover -s ./tests/integration -p 'test_*.py' -v