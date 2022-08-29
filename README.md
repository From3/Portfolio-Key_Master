# Python Key Master
<img border=0 src="https://img.shields.io/badge/python-3.8.1+-blue.svg?style=flat" alt="Python version"></a>
<a target="new" href="https://github.com/From3/Portfolio-Key_Master"><img border=0 src="https://img.shields.io/github/stars/From3/Portfolio-Key_Master.svg?style=social&label=Star&maxAge=60" alt="Star this repo"></a>

**Key Master** is a lightweight application written in Python 3 that allows to:
* generate passwords based on specified requirements
* check if provided passwords was ever leaked based on [Have I Been Pwned](https://haveibeenpwned.com/) API (which you can find out more about [here](https://haveibeenpwned.com/API/v3))
* store encrypted usernames and passwords in SQLite database and copy it's contents from application to use it wherever needed

## Installation

Install dependencies using `pip` from application's directory:

```
pip install -r requirements.txt
```

or in case multiple Python versions are installed:

```
pip3 install -r requirements.txt
```

## Usage

To use the app, run it from an IDE or a shell.

Run the app from shell:
```
python app.py
```
or in case multiple Python versions are installed:
```
python3 app.py
```
---

When running the app for the first time, it will ask to provide and confirm a master password which will be used in the future for loging in and encrypting/decrypting data. This password can be changed in app's `settings` tab.

Delete `profiles.db` file to remove all profiles and master password.
