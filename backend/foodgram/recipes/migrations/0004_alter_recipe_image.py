# Generated by Django 4.1.7 on 2023-03-03 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_quantity_ingredientrecipe_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/', verbose_name='Изображение'),
        ),
    ]