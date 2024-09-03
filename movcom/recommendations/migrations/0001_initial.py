# Generated by Django 5.0.6 on 2024-09-03 10:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_at', models.DateTimeField(auto_now_add=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('score', models.FloatField(default=0, help_text='Score based by the algorythm of recommendation')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_to', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
