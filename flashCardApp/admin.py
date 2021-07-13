from django.contrib import admin
from .models import Result,Case,CaseRes,MedTest, TestCat, ExamType,Loc 
# Register your models here.
admin.site.register(Result)

admin.site.register(Case)
admin.site.register(CaseRes)
admin.site.register(ExamType)
admin.site.register(MedTest)
admin.site.register(TestCat)
admin.site.register(Loc)