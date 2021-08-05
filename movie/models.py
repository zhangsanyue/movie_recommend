from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Movie(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # 一个电影只有一个分类
    title = models.CharField(max_length=128, help_text='Title')
    director = models.CharField(max_length=64, help_text='Director')
    writers = models.CharField(max_length=256, help_text='Writers')
    stars = models.CharField(max_length=512, help_text='Stars')
    storyline = models.CharField(max_length=1024, help_text='Storyline')
    average_star = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to='movie_images', blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class RecommendList(models.Model):
    title = models.CharField(max_length=128, help_text='Title')
    recommend_reason = models.CharField(max_length=10240, help_text='Title')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ManyToManyField(Movie, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username + self.title)
        super(RecommendList, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    content = models.CharField(max_length=9160)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class OAuth_type(models.Model):
    type_name = models.CharField(max_length = 12)
    title = models.CharField(max_length = 12)
    img = models.FileField(upload_to='static/img/connect')

    client_id = models.CharField(max_length = 24, default='')
    client_secret = models.CharField(max_length = 48, default='')
    redirect_uri = models.URLField(default='')
    scope = models.CharField(max_length = 24, default='')

    url_authorize = models.URLField(default='', blank=True)
    url_access_token = models.URLField(default='', blank=True)
    url_open_id = models.URLField(default='', blank=True)
    url_user_info = models.URLField(default='', blank=True)
    url_email = models.URLField(default='', blank=True)

    def __unicode__(self):
        return self.type_name


class OAuth_ex(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   #和User关联的外键
    openid = models.CharField(max_length=64)
    oauth_type = models.ForeignKey(OAuth_type, on_delete=models.CASCADE, default=1)  #关联账号的类型

    def __unicode__(self):
        return u'<%s>' % (self.user)


