# Generated by Django 3.0.6 on 2020-07-28 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20200608_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportproblem',
            name='problem',
            field=models.TextField(),
        ),
    ]