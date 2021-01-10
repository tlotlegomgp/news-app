# Mzansi News

https://mzansinews.herokuapp.com/

News hub web app. The app uses a free to use NEWS API to pull in all the news articles from different multiple sources across the world. Users can query the news they want by searching for articles by name, category, or news source.

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