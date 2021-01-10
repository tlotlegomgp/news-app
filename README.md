# Mzansi News

https://mzansinews.herokuapp.com/

A news articles website. Gathers all the headlines from all the major news networks. Users can sign up to get access to the site's search functionality, which allows them to search for news based on location, category, or topic. Made use of NEWS-API to make calls for the data.

Hosted on Heroku using a free plan. Site might take a moment to open on first launch.

### Tech stack:

* Python
* Django
* Bootstrap
* Heroku
* RESTFUL API

### How to run locally:

After cloning the app down to your machine, navigate into the root directory of the project. 

1. Install project requirements:
```Python
    pip install -r requirements.txt
```
2. Migrate and run project:
```Python
    python manage.py migrate
    python manage.py runserver
```
