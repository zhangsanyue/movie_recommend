import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_recommend.settings')

import django
django.setup()
from movie.models import *

def populate():
    categories = [
        {
            'name': 'comedy',
            'views': 20,
            'likes': 32,
            'movies': [
                'Space Jam: A New Legacy',
                'Never Have I Ever',
                'Rick and Morty',
            ]
        },
        {
            'name': 'sci-fi',
            'views': 15,
            'likes': 56,
            'movies': [
                'Black Widow',
                'Loki',
                'Dune',
            ]
        },
    ]


    for category in categories:
        cat = add_cat(category['name'], category['views'], category['likes'])
        for movie_title in category['movies']:
            movie_add(cat, movie_title)



def movie_add(cat, title, views=0):
    movie = Movie.objects.get_or_create(category=cat, title=title)[0]
    movie.views=views
    movie.director="Test Director"
    movie.writers="Test Writers"
    movie.stars="Test stars"
    movie.storyline="Test storyline"
    movie.average_star=5
    movie.save()
    return movie

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

if __name__ == '__main__':
    print('Starting movie population script...')
    populate()

