# Generated by Django 3.0.3 on 2020-04-15 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basicapp', '0006_auto_20200414_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
            preserve_default='True',
        ),
        migrations.AlterField(
            model_name='comments',
            name='user_comment',
            field=models.CharField(default='comment something', max_length=64),
        ),
    ]