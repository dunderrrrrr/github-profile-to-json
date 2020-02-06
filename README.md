github-profile-to-json
---
Export your Github profile (such as activity, repositories and profile info) to json or HTML using Python3 and Jinja2.  

## Screenshot 
```sh
$ python github.py -u github -o html
```
![HTML-output example](/helpers/img/readme/screenshot.png?raw=true "HTML-output example")

## Installation
Clone and cd into directory.
```sh
$ git clone git@github.com:dunderrrrrr/github-profile-to-json.git && cd github-profile-to-json
```
Create virtualenv and install requirements.
```sh
$ mkvirtualenv --python=/usr/bin/python3 github-profile
$ pip install -r requirements.txt
```

Copy `settings.py.sample` to `settings.py`.
```sh
$ cp settings.py.sample settings.py
$ nano settings.py
```

[Create a token](https://github.com/settings/tokens) and paste it in `settings.py`.  
When generating a token, make sure you tick **repo** and **user**-boxes to give the token read-access.
## Running
### Raw JSON output
```sh
$ python github.py -u <github_username>
```
### Pretty JSON output
```sh
$ python github.py -u <github_username> -o pretty
```
### HTML-file output
```sh
$ python github.py -u <github_username> -o html
```
