# Generated by Django 4.2.5 on 2023-09-19 09:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0008_documents_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documents",
            name="title",
            field=models.CharField(max_length=500),
        ),
    ]
