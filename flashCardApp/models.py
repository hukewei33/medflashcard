from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Loc(models.Model):
    name = models.CharField(max_length=200, unique = True)
    REGION_CHOICES = [("head and neck","head and neck"),("left upper limb","left upper limb"),("right upper limb","right upper limb"),("abdomen","abdomen"),("left chest","right chest"),("perineum","perineum"),("lower limb","lower limb"),("back","back")]
    region = models.CharField(max_length=200,choices=REGION_CHOICES,blank=True, null=True)
    def __str__(self):
        return self.name

# class TestCat(models.Model):
#     name = models.CharField(max_length=200, unique = True)
#     def __str__(self):
#         return self.name

class Action(models.Model):
    name = models.CharField(max_length=200, unique = True)
    # testcat = models.ForeignKey(TestCat, on_delete=models.CASCADE, blank=True, null=True)
    loc = models.ForeignKey(Loc, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Finding(models.Model):
    imagedata = models.ImageField(null = True, blank = True)
    audiodata = models.FileField(upload_to='audio', blank=True, null=True)
    des = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    default = models.BooleanField()
    def __str__(self):
        return self.name

class System(models.Model):
    name = models.CharField(max_length=200)
    actions = models.ManyToManyField(Action)
    def __str__(self):
        return self.name


class Case(models.Model):
    name = models.CharField(max_length=200)
    GENDER_CHOICES = [("M","male"),("F","female")]
    gender = models.CharField(max_length=200,choices=GENDER_CHOICES,blank=True, null=True)
    age = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(150)])
    findings = models.ManyToManyField(Finding, through='CaseRes')
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
    def group_results(self):
        res = self.imgs
        return res

class CaseRes(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    finding = models.ForeignKey(Finding, on_delete=models.CASCADE)
    #req = models.BooleanField()

    #from flashCardApp.models import Case, System,Action
    #c =Case.objects.filter(id =22 )