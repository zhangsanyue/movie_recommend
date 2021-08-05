import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_recommend.settings')

import json
import django
django.setup()
from movie.models import *


def populate():
    with open('data.json', 'r', encoding='utf-8') as f:
        categories = json.load(f)

    for category in categories:
        cat = add_cat(category['name'], category['views'], category['likes'])
        for movie in category['movies']:
            movie_add(cat,
                movie["average_star"],
                movie["director"],
                movie["likes"],
                movie["stars"],
                movie["storyline"],
                movie["title"],
                movie["views"],
                movie["writers"]
            )


def movie_add(cat, average_star, director, likes, stars, storyline, title, views, writers):
    movie = None
    try:
        movie = Movie.objects.get_or_create(category=cat, title=title)[0]
        movie.views = views
        movie.director = director
        movie.writers = writers
        movie.stars = stars
        movie.storyline = storyline
        movie.average_star = average_star
        # movie.likes = likes
        movie.save()
    except:
        pass
    return movie


# def movie_add(cat, title, views=0):
#     movie = Movie.objects.get_or_create(category=cat, title=title)[0]
#     movie.views=views
#     movie.director="Test Director"
#     movie.writers="Test Writers"
#     movie.stars="Test stars"
#     movie.storyline="Test storyline"
#     movie.average_star=5
#     movie.save()
#     return movie

def add_cat(name, views=0, likes=0):
    c = None
    try:
        c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
        c.save()
    except:
        pass
    return c


if __name__ == '__main__':
    print('Starting movie population script...')
    populate()

