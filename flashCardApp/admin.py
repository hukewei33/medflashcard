from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import fields,resources
from import_export.widgets import ForeignKeyWidget , ManyToManyWidget
#from .models import Finding,Case,CaseRes,Action, TestCat, System,Loc 
from .models import Finding,Case,CaseRes,Action,  System,Loc 
# Register your models here.
#admin.site.register(Result)
# admin.site.register(Case)
# admin.site.register(CaseRes)
# admin.site.register(System)
# admin.site.register(Action)
# admin.site.register(TestCat)
#admin.site.register(Loc)

@admin.register(Loc,Case,CaseRes)
class viewAdmin(ImportExportModelAdmin):
    pass

class ActionResource(resources.ModelResource):
    # testcat = fields.Field(
    #     column_name="testcat",
    #     attribute="testcat",
    #     widget=ForeignKeyWidget(TestCat, 'name'))
    loc = fields.Field(
        column_name="loc",
        attribute="loc",
        widget=ForeignKeyWidget(Loc, 'name'))
    class Meta:
        model = Action
        #fields = ("id","name",	"testcat",	"loc",)
        fields = ("id","name","loc",)

class ActionAdmin(ImportExportModelAdmin):
    resource_class = ActionResource

admin.site.register(Action, ActionAdmin)

class FindingResource(resources.ModelResource):
    action = fields.Field(
        column_name="action",
        attribute="action",
        widget=ForeignKeyWidget(Action, 'name'))
    
    class Meta:
        model = Finding
        fields = ("id","name",	"action",	"default",)

class FindingAdmin(ImportExportModelAdmin):
    resource_class = FindingResource

admin.site.register(Finding, FindingAdmin)


class SystemResource(resources.ModelResource):
    actions = fields.Field(
        column_name="actions",
        attribute="actions",
        widget=ManyToManyWidget(Action, field = "name"))
    
    class Meta:
        model = System
        fields = ("id","name",	"actions",	)

class SystemAdmin(ImportExportModelAdmin):
    resource_class = SystemResource

admin.site.register(System, SystemAdmin)