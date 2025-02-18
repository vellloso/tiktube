fazer o venv

pip install -r requirements.txt

python route.py

## Trabalhando com o BMVC no DOCKER:

1. $ docker build -t bmvci .
1. $ docker run -d -p 8080:8080 -v $(pwd):/app bmvci
