from django.contrib import admin
from .models import Employees, Department, Issues


# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position', 'department', 'manager']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class Emp_IssueAdmin(admin.TabularInline):
    model = Issues.employee.through
    extra = 0


class IssuesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'start_date', 'end_date']
    inlines = [Emp_IssueAdmin, ]


admin.site.register(Employees, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Issues, IssuesAdmin)
