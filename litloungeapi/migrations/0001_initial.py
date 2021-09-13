# Generated by Django 3.2.7 on 2021-09-13 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ReaderTalk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.reader')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=150)),
                ('identifier', models.CharField(max_length=50)),
                ('url_link', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WorkGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.genre')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.work')),
            ],
        ),
        migrations.AddField(
            model_name='work',
            name='genres',
            field=models.ManyToManyField(related_name='work', through='litloungeapi.WorkGenre', to='litloungeapi.Genre'),
        ),
        migrations.AddField(
            model_name='work',
            name='media_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.worktype'),
        ),
        migrations.AddField(
            model_name='work',
            name='posted_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='litloungeapi.reader'),
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=100)),
                ('sup_materials', models.CharField(max_length=250)),
                ('zoom_meeting_id', models.CharField(max_length=50)),
                ('zoom_meeting_password', models.CharField(max_length=50)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.reader')),
                ('participants', models.ManyToManyField(related_name='attending', through='litloungeapi.ReaderTalk', to='litloungeapi.Reader')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.work')),
            ],
        ),
        migrations.AddField(
            model_name='readertalk',
            name='talk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.talk'),
        ),
        migrations.CreateModel(
            name='ReaderGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.genre')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='litloungeapi.reader')),
            ],
        ),
        migrations.AddField(
            model_name='reader',
            name='genres',
            field=models.ManyToManyField(related_name='interest', through='litloungeapi.ReaderGenre', to='litloungeapi.Genre'),
        ),
        migrations.AddField(
            model_name='reader',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
