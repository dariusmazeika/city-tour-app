# Generated by Django 2.1.5 on 2019-01-15 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('flag', models.ImageField(blank=True, null=True, upload_to='languages')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('language', models.ForeignKey(default='lt', on_delete=django.db.models.deletion.CASCADE, to='translations.Language')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translations.Message')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='translation',
            unique_together={('message', 'language')},
        ),
    ]
