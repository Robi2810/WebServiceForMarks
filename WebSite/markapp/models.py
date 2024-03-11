from django.db import models


class Department(models.Model):
    dept_name = models.CharField(max_length=20, primary_key=True)
    building = models.CharField(max_length=40, null=True)
    budget = models.IntegerField(null=True)

    def __str__(self):
        return self.dept_name


class Group(models.Model):
    group_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=50, null=True)
    dept_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    credits = models.IntegerField(null=True)

    def __str__(self):
        return self.group_id


class Section(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    sec_id = models.CharField(primary_key=True, max_length=10)
    semester = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    section_buidling = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.sec_id


class Emploeye(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=10)
    emp_name = models.CharField(max_length=50)
    dept_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    tot_cred = models.IntegerField(null=True)

    def __str__(self):
        return self.emp_id


class EmploeyeSection(models.Model):
    emp_id = models.ForeignKey(Emploeye, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    sec_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    grade = models.CharField(max_length=6, null=True)


class Instructor(models.Model):
    instrustor_id = models.CharField(primary_key=True, max_length=10)
    instrustor_name = models.CharField(max_length=50, null=True)
    dept_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.IntegerField(null=True)

    def __str__(self):
        return self.instrustor_id


class GroupInstructor(models.Model):
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    sec_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
