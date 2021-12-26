# Generated by Django 2.2.6 on 2021-12-22 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20211222_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.Ingredient'),
        ),
        migrations.AlterField(
            model_name='quantity',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount', to='recipes.Recipe'),
        ),
    ]
