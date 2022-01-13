# Generated by Django 3.1.6 on 2021-03-23

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('translations', '0002_auto_20190709_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manifest_version', models.CharField(default='1', max_length=300)),
                ('default_language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_inform_language', to='translations.language')),
                ('enabled_languages', models.ManyToManyField(related_name='enabled_inform_languages', to='translations.Language')),
                ('password_renewal_template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='password_renewal_template', to='home.emailtemplate')),
                ('verify_email_template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verify_email_template', to='home.emailtemplate')),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplateTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField()),
                ('subject', models.CharField(max_length=100)),
                ('language', models.ForeignKey(default='lt', on_delete=django.db.models.deletion.SET_DEFAULT, to='translations.language')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_template_translations', to='home.emailtemplate')),
            ],
            options={
                'unique_together': {('template', 'language')},
            },
        ),
    ]