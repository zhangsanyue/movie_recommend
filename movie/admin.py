from django.contrib import admin
from movie.models import *
from movie.models import UserProfile
# Register your models here.


# class PageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


class RecommendListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(RecommendList, RecommendListAdmin)
admin.site.register(Review)
admin.site.register(UserProfile)
