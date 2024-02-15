from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blogs', '006_full_text_index_blog_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE FULLTEXT INDEX blog_title_description_index ON blogs_blog(title, description)",
            "DROP INDEX blog_title_description_index ON blogs_blog"
        ),
    ]
