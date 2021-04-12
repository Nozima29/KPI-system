from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

STATUS_CHOICES = (
    ('completed', 'завершено'),
    ('in progress', 'в прогрессе'),
    ('overdue', 'просроченно'),
    ('assigned', 'назначено'),
    ('new', 'новый'),
)


class Department(models.Model):
    name = models.CharField('Oтделение', max_length=100)

    class Meta:
        verbose_name = 'Oтделение'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=100)
    position = models.CharField('Должность', max_length=100)
    department = models.ForeignKey(Department, related_name='employee_department', verbose_name='Oтделение',
                                   on_delete=models.CASCADE)
    manager = models.ForeignKey('self', verbose_name='Менеджер', null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='subordinate')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.name


class Issues(models.Model):
    name = models.CharField('Задача', max_length=255)
    description = models.TextField('Описание')
    start_date = models.DateTimeField('Дата начала', default=timezone.now)
    end_date = models.DateTimeField('Дата окончания', null=True, blank=True)
    status = models.CharField('Статус', choices=STATUS_CHOICES, default='new', max_length=20)
    file = models.FileField('Файл (если не обходимо)', blank=True, null=True)
    employee = models.ManyToManyField(Employees, verbose_name='Назначить на', related_name='issue_employee')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.name

