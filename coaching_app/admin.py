from django.contrib import admin
from .models import Student, Coach, Team, Tag

# Register your models here.

admin.site.register(Student)
admin.site.register(Coach)
admin.site.register(Team)
admin.site.register(Tag)