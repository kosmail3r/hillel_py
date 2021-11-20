from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


def default_time():
    return timezone.now() + timezone.timedelta(+2)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=280)),
                ('posted', models.BooleanField()),
                ('brief_description', models.CharField(max_length=250)),
                ('full_description', models.CharField(max_length=1350)),
                ('published_date', models.DateTimeField(null=True, default=default_time())),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('text', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_blog.post')),
            ],
        ),
    ]
