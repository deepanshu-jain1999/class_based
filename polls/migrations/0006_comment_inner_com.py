# Generated by Django 2.0.2 on 2018-02-17 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='inner_com',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inner_comment', to='polls.Comment'),
        ),
    ]
