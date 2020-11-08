# Generated by Django 2.2.12 on 2020-06-03 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(blank=True, max_length=100)),
                ('image', models.CharField(blank=True, max_length=500)),
                ('article', models.TextField(blank=True)),
            ],
        ),
    ]