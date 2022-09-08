# Meme generator

## Setup

Packages:
```console
pip install flask
sudo apt-get install -y xpdf
```

## Run

```console
export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload
```

If you have multiple Python versions see
[stackoverflow](https://stackoverflow.com/questions/49255283/run-flask-using-python3-not-python).

Or you can install anaconda and run:
```console
source ~/anaconda3/bin/activate root
export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload
```
