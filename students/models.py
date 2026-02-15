from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    photo = models.ImageField(upload_to="student_photos/", null=True, blank=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)  # Present / Absent
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.status}"

