# Generated by Django 2.0.2 on 2018-02-15 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeProfile',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.Profile')),
                ('like_status', models.IntegerField(default=0)),
                ('like_time', models.DateTimeField(auto_now_add=True)),
                ('like_user', models.ManyToManyField(blank=True, related_name='liked_user', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('polls.profile',),
        ),
    ]