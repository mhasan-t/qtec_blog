from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blogs', '0005_rename_details_blog_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE FULLTEXT INDEX blog_description_index ON blogs_blog(description)",
            "DROP INDEX blog_description_index ON blogs_blog"
        ),
    ]
