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

class OAuthTypeAdmin(admin.ModelAdmin):
    list_display=('id','type_name', 'title', 'img')

    fieldsets = (
        (u'OAuth type', {
            "fields":('type_name', 'title', 'img')
            }),
        (u'OAuth config', {
            "fields":('client_id','client_secret','redirect_uri','scope')
            }),
        (u'OAuth url', {
            "fields":('url_authorize','url_access_token','url_open_id','url_user_info','url_email')
            })
    )

class OAuthAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'openid', 'oauth_type')


admin.site.register(OAuth_ex, OAuthAdmin)
admin.site.register(OAuth_type, OAuthTypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(RecommendList, RecommendListAdmin)
admin.site.register(Review)
admin.site.register(UserProfile)
