from django.test import TestCase
from .models import Employees, Department, Issues
from django.db.models import Q

# Create your tests here.


class TestQuery(TestCase):
    def setUp(self) -> None:
        self.dep = Department.objects.create(name='IT')
        self.dep1 = Department.objects.create(name='Marketing')
        self.dep2 = Department.objects.create(name='HR')

        self.emp = Employees.objects.create(
            name='Nozi',
            position='backend',
            department=self.dep
        )
        self.emp1 = Employees.objects.create(
            name='Dilbar',
            position='frontend',
            department=self.dep
        )
        self.emp2 = Employees.objects.create(
            name='Aziza',
            position='content',
            department=self.dep1
        )

        self.issue = Issues.objects.create(
            name='database',
            description='sss',
            status='assigned'
        )
        self.issue.employee.add(self.emp)
        self.issue = Issues.objects.create(
            name='design',
            description='sss',
            status='completed'
        )
        self.issue.employee.add(self.emp1)

    def test_get_issue_by_dept(self):
        emp_in_IT = Employees.objects.filter(department=self.dep).values_list('id')
        issue_by_dept = Issues.objects.filter(employee__in=emp_in_IT).count()
        #print(issue_by_dept)

        emp_in_Markting = Employees.objects.filter(department=self.dep1).values_list('id')
        issue_by_dept = Issues.objects.filter(employee__in=emp_in_Markting).count()
        #print(issue_by_dept)

    def test_dept_performance(self):
        emp_in_IT = Employees.objects.filter(department=self.dep).values_list('id')
        all_issue_by_dept = Issues.objects.filter(employee__in=emp_in_IT).count()
        done_issues_by_dept = Issues.objects.filter(Q(employee__in=emp_in_IT) & Q(status='completed')).count()
        performance = done_issues_by_dept * 100 / all_issue_by_dept
        #print(performance)

    def test_emp_performance(self):
        emp = Employees.objects.filter(department=self.dep)
        emp_perf = {}
        for e in emp:
            done_issues = Issues.objects.filter(Q(employee=e) & Q(status='completed')).count()
            emp_perf[e.name] = done_issues * 100 / Issues.objects.filter(employee=e).count()
        print(emp_perf)

