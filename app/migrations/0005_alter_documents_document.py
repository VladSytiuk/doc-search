# Generated by Django 4.2.5 on 2023-09-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_alter_documents_document"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documents",
            name="document",
            field=models.FileField(unique=True, upload_to=""),
        ),
    ]