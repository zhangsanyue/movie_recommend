from django.urls import path
from movie import views


app_name = 'movie'


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('categories/', views.categories, name='categories'),
    path('category/<slug:category_name_slug>/', views.category, name='category'),
    path('category_add/', views.category_add, name='category_add'),
    path('category/<slug:category_name_slug>/movie_add/', views.movie_add, name='movie_add'),

    path('movie/<slug:movie_name_slug>/', views.show_movie, name='show_movie'),

    path('me/', views.me, name='me'),
    path('me/recommend_list/<slug:recommend_list_slug>', views.recommend_list, name='recommend_list'),
    path('me/recommend_list_add/', views.recommend_list_add, name='recommend_list_add'),
    path('me/recommend_list/<slug:recommend_list_slug>/add_movie', views.recommend_list_add_movie,
         name='recommend_list_add_movie'),

    path('user/<slug:user_name>', views.other_user_profile,
         name='other_user_profile'),
    path('oauth_login/', views.oauth_login, name='oauth_login'),

    path('github_check/', views.github_check, name='github_check'),

    path('bind_email/', views.bind_email, name='bind_email'),
]
