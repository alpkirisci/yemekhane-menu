# Generated by Django 4.2.15 on 2024-08-23 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_ingredientitem_remove_ingredient_quantitiy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='served_at',
            field=models.DateField(unique_for_date=True),
        ),
    ]
