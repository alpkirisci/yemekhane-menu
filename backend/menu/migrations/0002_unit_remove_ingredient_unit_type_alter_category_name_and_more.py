# Generated by Django 4.2.15 on 2024-08-18 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='unit_type',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_daily_menus', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='servings',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='dailymenu',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_daily_menus', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ingredientname',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_menu_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='description',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_menu_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UnitType',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.unit'),
        ),
    ]
