from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget , ManyToManyWidget
from .models import Result,Case,CaseRes,MedTest, TestCat, ExamType,Loc 
# Register your models here.
#admin.site.register(Result)
# admin.site.register(Case)
# admin.site.register(CaseRes)
# admin.site.register(ExamType)
# admin.site.register(MedTest)
# admin.site.register(TestCat)
#admin.site.register(Loc)

@admin.register(Loc,Case,CaseRes,TestCat)
class viewAdmin(ImportExportModelAdmin):
    pass

class MedTestResource(resources.ModelResource):
    testcat = fields.Field(
        column_name="testcat",
        attribute="testcat",
        widget=ForeignKeyWidget(TestCat, 'name'))
    loc = fields.Field(
        column_name="loc",
        attribute="loc",
        widget=ForeignKeyWidget(Loc, 'name'))
    class Meta:
        model = MedTest
        fields = ("id","name",	"testcat",	"loc",)

class MedTestAdmin(ImportExportModelAdmin):
    resource_class = MedTestResource

admin.site.register(MedTest, MedTestAdmin)

class ResultResource(resources.ModelResource):
    medTest = fields.Field(
        column_name="medTest",
        attribute="medTest",
        widget=ForeignKeyWidget(MedTest, 'name'))
    
    class Meta:
        model = Result
        fields = ("id","name",	"medTest",	"default",)

class ResultAdmin(ImportExportModelAdmin):
    resource_class = ResultResource

admin.site.register(Result, ResultAdmin)


class ExamTypeResource(resources.ModelResource):
    medtests = fields.Field(
        column_name="medtests",
        attribute="medtests",
        widget=ManyToManyWidget(MedTest, field = "name"))
    
    class Meta:
        model = ExamType
        fields = ("id","name",	"medtests",	)

class ExamTypeAdmin(ImportExportModelAdmin):
    resource_class = ExamTypeResource

admin.site.register(ExamType, ExamTypeAdmin)