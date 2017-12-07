from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.UserInfo)
admin.site.register(models.Question)
admin.site.register(models.Questionnaire)
admin.site.register(models.Student)
admin.site.register(models.Class)
admin.site.register(models.Answer)
admin.site.register(models.Option)
