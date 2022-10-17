# Generated by Django 3.2.5 on 2022-05-25 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(verbose_name='리뷰분석')),
            ],
            options={
                'verbose_name': '리뷰분석',
                'verbose_name_plural': '리뷰분석',
            },
        ),
        migrations.CreateModel(
            name='Kakao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField(verbose_name='x')),
                ('y', models.FloatField(verbose_name='y')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.search', verbose_name='목적지')),
            ],
            options={
                'verbose_name': '위도-경도',
                'verbose_name_plural': '위도-경도',
            },
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, verbose_name='이미지 주소')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.search', verbose_name='목적지')),
            ],
            options={
                'verbose_name': '이미지',
                'verbose_name_plural': '이미지',
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='제목')),
                ('contents', models.TextField(verbose_name='내용')),
                ('scope', models.CharField(max_length=10, verbose_name='별점')),
                ('register_dttm', models.CharField(max_length=100, verbose_name='등록날짜')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.search', verbose_name='목적지')),
            ],
            options={
                'verbose_name': '리뷰',
                'verbose_name_plural': '리뷰',
            },
        ),
    ]
