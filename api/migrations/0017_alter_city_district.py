# Generated by Django 4.2.6 on 2024-02-10 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_city_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.district'),
        ),
    ]
