# acg

Make own API client for particular API interface/server with only one configuration file. 
Then use it in development. For further details look down.

[![Release](https://img.shields.io/github/release/dmytrostriletskyi/acg.svg)](https://github.com/dmytrostriletskyi/acg/releases)
![Python3](https://img.shields.io/badge/Python-2.7-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.5-brightgreen.svg)
![Python3](https://img.shields.io/badge/Python-3.6-brightgreen.svg)

# Gettings started

## What is acg?

ACG allows you to create you API client (wrapper around some API) and use it in Python code in few minutes after install.

For example, you have some back-end server called `Google API` with address `https://google.com/api/v1` and
one front-end server, that grab data from back-end server or only push data to it.

Next task: you want to work with user subject, you do it with `https://google.com/api/v1/user` API url.

Some API endpoints:
* get user: request to `https://google.com/api/v1/user` with method `get` and param `id`.
* create user: request to `https://google.com/api/v1/user` with method `post` and params `id, name, surname`.
* create user castle: request to `https://google.com/api/v1/user/castle` with method `post` and params `id, castle`.

Without ACG:

```python
import requests 


create_jon_snow_user = requests.post('https://google.com/api/v1/user', params={
    'id': 7,
    'name': 'Jon',
    'surname': Snow,
})

get_jon_snow_user = requests.get('https://google.com/api/v1/user', params={'id': 7})

create_jon_snow_castle = requests.post('https://google.com/api/v1/user/castle', params={
    'id': 7,
    'castle': 'Winterfell',
})
```

Using ACG:

```python
from google_api import google_api_client


create_jon_snow_user = google_api_client.user.create({
    'id': 7,
    'name': 'Jon',
    'surname': Snow
})

get_jon_snow_user = google_api_client.user.get({'id': 7})

create_jon_snow_castle = google_api_client.user.castle.create({
    'id': 7,
    'castle': 'Winterfell',
})
```

## How it works

* you need to create configuration file named as `.acg.yml`.

```
pypi:
  username: dmytrostriletskyi
  password: d843rnd3

acg:
  name: google_api
  version: 0.1.5

  api: https://google.com/api/v1

  services:
    user:
      url: /user
      endpoints: create:post, get:get

    user.castle:
      url: /user/castle
      endpoints: create:post
```

Why it need `PyPi` credentials? `acg` deploy your API client to the `Python Package Index` to account based on credentials.

Then you will be able to install your API client with pip - `pip install {name}`.
`{name}` is the first point in `acg` cause in configuration file (in example it is `google_api`).

* if you finished configuring a file, type `acg` to terminal (after installation a `acg` package of course).
* remember to up version in configuration file if you edit it and want to update API client.
* you can use any `HTTP-methods` and put any data to it, because `acg` based on `requests` library.
* endpoints needs to be separated by comma.
* one endpoint's cause contains end of client sequence and `http-method` type (e.g. `create:post`).

After all of that you can import API client to code:

```python
from google_api import google_api_client
```

Client module is always based on `{name}_client`.
If you called your package as `Hello`, you are able import client following next code:

```python
from Hello import Hello_client
```

## Install

Following command in your terminal (you are able to use `pip3`):

```
pip install acg
```

Or install source code and follow this:

```
python setup.py install
```
