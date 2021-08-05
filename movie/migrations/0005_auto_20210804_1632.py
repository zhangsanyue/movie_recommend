# Generated by Django 2.1.5 on 2021-08-04 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0004_auto_20210801_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuth_ex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='OAuth_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=12)),
                ('title', models.CharField(max_length=12)),
                ('img', models.FileField(upload_to='static/img/connect')),
                ('client_id', models.CharField(default='', max_length=24)),
                ('client_secret', models.CharField(default='', max_length=48)),
                ('redirect_uri', models.URLField(default='')),
                ('scope', models.CharField(default='', max_length=24)),
                ('url_authorize', models.URLField(blank=True, default='')),
                ('url_access_token', models.URLField(blank=True, default='')),
                ('url_open_id', models.URLField(blank=True, default='')),
                ('url_user_info', models.URLField(blank=True, default='')),
                ('url_email', models.URLField(blank=True, default='')),
            ],
        ),
        migrations.AddField(
            model_name='oauth_ex',
            name='oauth_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movie.OAuth_type'),
        ),
        migrations.AddField(
            model_name='oauth_ex',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
