from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Employees, Department, Issues
from django.db.models import Q
from django.contrib.auth.models import User
from faker import Faker
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import *


# Create your views here.

def populate_data():
    status_choices = ['completed', 'in progress', 'overdue', 'assigned', 'new']
    depart = Department.objects.all()
    fake = Faker()
    for i in range(20):
        Employees.objects.create(
            name=fake.name(),
            position=fake.job(),
            department=random.choice(depart),
        )
        i += 1
    emp = Employees.objects.all()
    for i in range(30):
        issue = Issues.objects.create(
            name=fake.job(),
            description=fake.text(max_nb_chars=200),
            start_date=fake.date_time(),
            end_date=fake.date_time(),
            status=random.choice(status_choices),
        )
        issue.employee.add(random.choice(emp))
        issue.save()
        i += 1


def index(request):
    populate_data()
    return HttpResponse('main app')

class UserRegister(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        

class CreateDepartment(APIView):
    serializer_class = DepartmentSerializer

    def get(self, request):
        depts = [{'id': dept.id, 'name': dept.name} for dept in Department.objects.all()]
        return Response(depts)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class DeleteDepartment(APIView):
    serializer_class = DepartmentSerializer

    def get(self, request):
        depts = [{'id': dept.id, 'name': dept.name} for dept in Department.objects.all()]
        return Response(depts)

    def post(self, request):
        dept = Department.objects.get(id=request.data['name'])
        dept.delete()
        return Response('Department deleted')


class CreateEmployeeView(APIView):
    serializer_class = EmployeeSerializer

    def get(self, request):
        emps = [{'id': emp.id, 'name': emp.name, 'department': emp.department,
                 'position': emp.position, 'manager': emp.manager}
                for emp in Employees.objects.all()]
        return Response(emps)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class UpdateEmployeeView(APIView):
    serializer_class = EmployeeSerializer

    def get(self, request, id):
        emp = Employees.objects.get(id=id)
        emp = [{'id': emp.id, 'position': emp.position, 'manager': emp.manager}]
        return Response(emp)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     print(instance)
    #     serializer = self.serializer_class(data=request.data)
    #     name = serializer.validated_data.get('name')
    #
    #     return Response(name)


class AllDepartmentsView(APIView):

    def get(self, request):
        emp_it = Employees.objects.filter(department=1).values_list('id')
        emp_markt = Employees.objects.filter(department=2).values_list('id')
        emp_hr = Employees.objects.filter(department=3).values_list('id')
        emp_cc = Employees.objects.filter(department=4).values_list('id')
        emp_ac = Employees.objects.filter(department=5).values_list('id')
        context, performances = {}, []

        all_issue_it = Issues.objects.filter(employee__in=emp_it).count()
        if all_issue_it:
            performances.append(Issues.objects.filter(Q(employee__in=emp_it) & Q(status='completed')).count() *
                                100 / all_issue_it)
        else:
            performances.append(0)

        all_issue_markt = Issues.objects.filter(employee__in=emp_markt).count()
        if all_issue_markt:
            performances.append(Issues.objects.filter(
                Q(employee__in=emp_markt) & Q(status='completed')).count() * 100 / all_issue_markt)
        else:
            performances.append(0)

        all_issue_hr = Issues.objects.filter(employee__in=emp_hr).count()
        if all_issue_hr:
            performances.append(Issues.objects.filter(Q(employee__in=emp_hr) & Q(status='completed')).count()
                                * 100 / all_issue_hr)
        else:
            performances.append(0)

        all_issue_cc = Issues.objects.filter(employee__in=emp_cc).count()
        if all_issue_cc:
            performances.append(Issues.objects.filter(Q(employee__in=emp_cc) & Q(status='completed')).count()
                                * 100 / all_issue_cc)
        else:
            performances.append(0)

        all_issue_ac = Issues.objects.filter(employee__in=emp_ac).count()
        if all_issue_ac:
            performances.append(Issues.objects.filter(Q(employee__in=emp_ac) & Q(status='completed')).count()
                                * 100 / all_issue_ac)
        else:
            performances.append(0)

        i = 0
        for dept in Department.objects.all():
            context[dept.name] = performances[i]
            i += 1

        return Response(context)


class SingleDepartmentView(APIView):

    def get(self, request, id):
        emp_by_department = Employees.objects.filter(department=id).values_list('id')
        dep_issues = Issues.objects.filter(employee__in=emp_by_department)
        done_issues = dep_issues.filter(status='completed').count()
        # serialized = serializers.serialize('json', emp_by_department, fields=('name', 'department'))
        context = {
            'issues': dep_issues.values_list('name').count(),
            'done': done_issues,
        }
        return Response(context)


class EmployeePerformanceByDepartment(APIView):

    def get(self, request, id):
        emp = Employees.objects.filter(department=id)
        context = {}
        for e in emp:
            done_issues = Issues.objects.filter(Q(employee=e) & Q(status='completed')).count()
            if not Issues.objects.filter(employee=e):
                context[e.name] = 0
            else:
                context[e.name] = done_issues * 100 / Issues.objects.filter(employee=e).count()

        return Response(context)


class DepartmentIssuesView(APIView):
    serializer_class = IssuesSerializer

    def get(self, request, id):
        issues = Issues.objects.filter(employee__department_id=id)
        emps = issues.values_list('employee__name')
        issue = [{'id': i.id, 'name': i.name, 'status': i.status,
                  'start_date': i.start_date, 'end_date': i.end_date, 'employee': i.employee} for i in issues]
        return Response(issue)


class DepartmentMonthlyPerformance(APIView):
    def get(self, request):
        import datetime
        context = {}
        today = datetime.datetime.now()
        month1 = today.month - 3
        year1 = today.year
        issue_by_dept = Issues.objects.prefetch_related('employee__department')
        # for m in range(12):
        issues = issue_by_dept.filter(
            start_date__year__gte=year1,
            start_date__month__gte=month1
        )
        #   tot_issues = issues.count()

        issue = [{'name': i.name, 'start_date': i.start_date} for i in issues]
        return Response(issue)
