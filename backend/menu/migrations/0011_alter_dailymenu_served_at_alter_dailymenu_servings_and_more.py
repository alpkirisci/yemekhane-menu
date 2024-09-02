# Generated by Django 4.2.15 on 2024-09-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_alter_dailymenu_servings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailymenu',
            name='served_at',
            field=models.DateField(unique=True),
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='servings',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('g', 'Gram'), ('ml', 'Milliliter'), ('p', 'Piece(s)')], max_length=50),
        ),
    ]