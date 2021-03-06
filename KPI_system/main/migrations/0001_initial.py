# Generated by Django 3.1.7 on 2021-04-12 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Oтделение')),
            ],
            options={
                'verbose_name': 'Oтделение',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('position', models.CharField(max_length=100, verbose_name='Должность')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_department', to='main.department', verbose_name='Oтделение')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinate', to='main.employees', verbose_name='Менеджер')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Задача')),
                ('description', models.TextField(verbose_name='Описание')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')),
                ('status', models.CharField(choices=[('completed', 'завершено'), ('in progress', 'в прогрессе'), ('overdue', 'просроченно'), ('assigned', 'назначено'), ('new', 'новый')], default='new', max_length=20, verbose_name='Статус')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл (если не обходимо)')),
                ('employee', models.ManyToManyField(related_name='issue_employee', to='main.Employees', verbose_name='Назначить на')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задания',
            },
        ),
    ]
