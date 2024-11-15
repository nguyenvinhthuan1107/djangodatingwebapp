# Generated by Django 5.1.2 on 2024-10-27 04:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_user_is_active_user_is_staff"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DatingProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("gender", models.CharField(max_length=10)),
                ("age", models.PositiveIntegerField()),
                ("bio", models.TextField(blank=True, max_length=500)),
                ("location", models.CharField(max_length=100)),
                ("interests", models.CharField(blank=True, max_length=200)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
