# Generated by Django 5.2 on 2025-05-07 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedHRData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('department', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('age', models.FloatField()),
                ('education', models.CharField(max_length=100)),
                ('salary', models.FloatField()),
                ('tenure', models.FloatField()),
                ('satisfaction', models.FloatField()),
                ('absent_days', models.FloatField()),
                ('promotion', models.BooleanField()),
            ],
        ),
    ]
