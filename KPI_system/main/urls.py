from django.urls import path
from .views import *
# from rest_framework import routers
#
# router = routers.DefaultRouter()


urlpatterns = [
    path('', index),

    #data visualisation <get>
    path('department/<int:id>/', SingleDepartmentView.as_view(), name='department'),
    path('employee_in_dept/<int:id>/', EmployeePerformanceByDepartment.as_view(), name='employees'),
    path('all_dept/', AllDepartmentsView.as_view(), name='departments'),
    path('issue_in_dept/<int:id>/', DepartmentIssuesView.as_view()),
    path('dept_by_month/', DepartmentMonthlyPerformance.as_view()),

    #admin CRUD system <get/post>
    path('create_dept/', CreateDepartment.as_view(), name='create_dept'),
    path('create_employee/', CreateEmployeeView.as_view(), name='employee'),

    path('delete_dept/', DeleteDepartment.as_view(), name='delete_dept'),

    path('update_employee/<int:id>/', UpdateEmployeeView.as_view(), name='update_emp'),
]