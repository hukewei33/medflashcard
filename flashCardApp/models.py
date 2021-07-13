from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Loc(models.Model):
    name = models.CharField(max_length=200)
    # top = models.PositiveIntegerField(default=0)
    # left = models.PositiveIntegerField(default=0)
    REGION_CHOICES = [("head","head"),("forearm","forearm"),("palm","palm"),("chest","chest"),("pelvis","pelvis"),("legs","legs")]
    region = models.CharField(max_length=200,choices=REGION_CHOICES,blank=True, null=True)
    def __str__(self):
        return self.name

class TestCat(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class MedTest(models.Model):
    name = models.CharField(max_length=200)
    testcat = models.ForeignKey(TestCat, on_delete=models.CASCADE, blank=True, null=True)
    loc = models.ForeignKey(Loc, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

class Result(models.Model):
    data = models.ImageField(null = True, blank = True)
    audiodata = models.FileField(upload_to='audio', blank=True, null=True)
    des = models.CharField(max_length=200)
    name = models.CharField(max_length=200, blank=True, null=True)
    medTest = models.ForeignKey(MedTest, on_delete=models.CASCADE, blank=True, null=True)
    default = models.BooleanField(blank=True, null=True)
    def __str__(self):
        return self.name

class ExamType(models.Model):
    name = models.CharField(max_length=200)
    medtests = models.ManyToManyField(MedTest)
    def __str__(self):
        return self.name


class Case(models.Model):
    name = models.CharField(max_length=200)
    GENDER_CHOICES = [("M","male"),("F","female")]
    gender = models.CharField(max_length=200,choices=GENDER_CHOICES,blank=True, null=True)
    age = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(150)])
    result = models.ManyToManyField(Result, through='CaseRes')
    examtype = models.ForeignKey(ExamType, on_delete=models.CASCADE, blank=True, null=True)
    diagnosis = models.CharField(max_length=200,blank=True, null=True)
    def __str__(self):
        return self.name
    
    def group_results(self):
        res = self.imgs
        return res

class CaseRes(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    req = models.BooleanField()