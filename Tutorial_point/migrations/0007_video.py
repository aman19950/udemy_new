# Generated by Django 3.1.14 on 2022-07-05 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutorial_point', '0006_course_dtls_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=200)),
                ('s_no', models.IntegerField()),
                ('video_id', models.CharField(max_length=200)),
                ('is_preview', models.BooleanField(default=False)),
                ('course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorial_point.course_dtls')),
            ],
        ),
    ]