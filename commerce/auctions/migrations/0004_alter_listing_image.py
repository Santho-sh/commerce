# Generated by Django 4.1.6 on 2023-02-17 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_bids_bid_rename_comments_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(default=None, upload_to='images'),
        ),
    ]
