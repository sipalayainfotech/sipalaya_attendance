from django.contrib import admin
admin.site.site_header = "Sipalaya Attendance System"
# Register your models here.
from .models import *
admin.site.register([Employee,Instructor,Group,Student,Attendance,StudentAttendanceSummary])