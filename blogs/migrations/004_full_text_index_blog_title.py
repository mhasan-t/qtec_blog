from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blogs', '0003_blog_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE FULLTEXT INDEX blog_title_index ON blogs_blog(title)",
            "DROP INDEX blog_title_index ON blogs_blog"
        ),
    ]
