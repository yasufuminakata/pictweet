# Generated by Django 4.2.10 on 2025-06-04 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_rename_text_tweet_memo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='memo',
            new_name='text',
        ),
    ]
