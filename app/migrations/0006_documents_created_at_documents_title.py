# Generated by Django 4.2.5 on 2023-09-15 06:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_alter_documents_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="documents",
            name="created_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="documents",
            name="title",
            field=models.CharField(default="ddd", max_length=500, unique=True),
            preserve_default=False,
        ),
    ]
