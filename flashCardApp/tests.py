from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIRequestFactory,force_authenticate
from .models import Case,CaseRes,System,Action,Finding,Loc
from django.contrib.auth.models import User
from . import views
from collections import OrderedDict
# Create your tests here.
def create_context():
    #create user
    user=User.objects.create_user('foo', password='bar')
    user.is_superuser=True
    user.is_staff=True
    user.save()
    
    loc1 = Loc.objects.create(name = "loc1", region = "head and neck")
    loc2 = Loc.objects.create(name = "loc2", region = "upper limb")
    a1 = Action.objects.create(name= "action1" , loc = loc1)
    a2 = Action.objects.create(name= "action2" , loc = loc1)
    a3 = Action.objects.create(name= "action3" , loc = loc2)
    s1 = System.objects.create(name = "system1")
    s2 = System.objects.create(name = "system2")
    s1.actions.add(a1,a2)
    s2.actions.add(a3,a2)
    f11 = Finding.objects.create(name = "finding1-1", action =a1, default = True )
    f12 = Finding.objects.create(name = "finding1-2", action =a1, default = False )
    f21 = Finding.objects.create(name = "finding2-1", action =a2, default = True )
    f22 = Finding.objects.create(name = "finding2-2", action =a2, default = False )
    f31 = Finding.objects.create(name = "finding3-1", action =a3, default = True )
    f32 = Finding.objects.create(name = "finding3-2", action =a3, default = False )
    c1 = Case.objects.create(name = "case1", gender = "F" , diagnosis = "not important", age = 34, system = s1)
    c2 = Case.objects.create(name = "case2", gender = "M" , diagnosis = "not important also" ,age = 4 ,system = s2)
    CaseRes.objects.create(case = c1, finding = f11)
    CaseRes.objects.create(case = c1, finding = f22)
    CaseRes.objects.create(case = c2, finding = f31)
    CaseRes.objects.create(case = c2, finding = f21)


class IndexSystemTests(APITestCase):
    #list all systems
    def test_index_system(self):
        create_context()
        response = self.client.get(reverse('system-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': 1, 'name': 'system1'},{'id': 2, 'name': 'system2'}])

    #index all default findings
    def test_index_def_finding(self):
        create_context()
        response = self.client.get(reverse("def-finding-list"), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),3)
        #print(response.data)
        self.assertEqual(response.data,[
            {"id":1 ,'imagedata': None, 'audiodata': None, 'des': None, 'name': 'finding1-1', 'default': True , 'action' :{"id":1 , "name": "action1", "loc":{'id':1,'name':"loc1", "region" : "head and neck"}}},
            {"id":3 ,'imagedata': None, 'audiodata': None, 'des': None, 'name': 'finding2-1', 'default': True , 'action' :{"id":2 , "name": "action2" ,"loc":{'id':1,'name':"loc1", "region":"head and neck"}}},
            {"id":5 ,'imagedata': None, 'audiodata': None, 'des': None, 'name': 'finding3-1', 'default': True , 'action' :{"id":3 , "name": "action3" ,"loc":{'id':2,'name':"loc2", "region":"upper limb"}}}
        ])
    
    #index all cases with system info

    def test_index_cases(self):
        create_context()
        response = self.client.get(reverse("case-list"), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),2)
        self.assertEqual(response.data,[OrderedDict([('id', 2), ('system', OrderedDict([('name', 'system2'), ('id', 2)])), ('name', 'case2'), ('gender', 'M'), ('age', 4), ('diagnosis', 'not important also'), ('findings', [5, 3])]), OrderedDict([('id', 1), ('system', OrderedDict([('name', 'system1'), ('id', 1)])), ('name', 'case1'), ('gender', 'F'), ('age', 34), ('diagnosis', 'not important'), ('findings', [1, 4])])])
    #see a specific test
    def test_show_cases(self):
        create_context()
        response = self.client.get(reverse("case-detail", args = [1]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
        self.assertEqual(response.data,
       {'id': 1, 'name': 'case1', 'gender': 'F', 'age': 34, 'caseres_set': [OrderedDict([('id', 1), ('finding', OrderedDict([('id', 1), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding1-1'), ('default', True), ('action', OrderedDict([('id', 1), ('name', 'action1'), ('loc', OrderedDict([('id', 1), ('name', 'loc1'), ('region', 'head and neck')]))]))]))]), OrderedDict([('id', 2), ('finding', OrderedDict([('id', 4), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding2-2'), ('default', False), ('action', OrderedDict([('id', 2), ('name', 'action2'), ('loc', OrderedDict([('id', 1), ('name', 'loc1'), ('region', 'head and neck')]))]))]))])], 'diagnosis': 'not important'}
        )
    #index all caseres for each case
    def test_show_case_res_cases(self):
        create_context()
        response = self.client.get(reverse("case-res", args = [1]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
        self.assertEqual(response.data,{'caseres_set': [OrderedDict([('id', 1), ('finding', OrderedDict([('id', 1), ('action', OrderedDict([('name', 'action1'), ('finding_set', [OrderedDict([('id', 1), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding1-1'), ('default', True), ('action', 1)]), OrderedDict([('id', 2), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding1-2'), ('default', False), ('action', 1)])]), ('loc', OrderedDict([('id', 1), ('name', 'loc1'), ('region', 'head and neck')]))])), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding1-1'), ('default', True)]))]), OrderedDict([('id', 2), ('finding', OrderedDict([('id', 4), ('action', OrderedDict([('name', 'action2'), ('finding_set', [OrderedDict([('id', 3), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding2-1'), ('default', True), ('action', 2)]), OrderedDict([('id', 4), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding2-2'), ('default', False), ('action', 2)])]), ('loc', OrderedDict([('id', 1), ('name', 'loc1'), ('region', 'head and neck')]))])), ('imagedata', None), ('audiodata', None), ('des', None), ('name', 'finding2-2'), ('default', False)]))])], 'name': 'case1', 'gender': 'F', 'diagnosis': 'not important', 'age': 34,"system": 1,"id":1})

    def test_case_update(self):
        create_context()
        data = {'name':'case1 updated', 'age':"11","gender":"M","diagnosis":"changed diagnosis"}
        response = self.client.patch(reverse("case-update",args = [1]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Case.objects.count(), 2)
        #print(response.data)
        self.assertEqual(response.data, {'id': 1, 'name': 'case1 updated', 'gender': 'M', 'age': 11, 'diagnosis': 'changed diagnosis', 'system': 1, 'findings': [1, 4]})

   



class OtherCaseTest(APITestCase):
    #create a case and create a realtionship with all its default findings for all its tests
    def test_create_case(self):
        #Ensure we can create a new case.
        factory = APIRequestFactory()
        view = views.caseCreate
        create_context()
        user = User.objects.get(username='foo') 
        cnt = 1
        for sysId,res in[(1,[1,3]),(2,[3,5])] :
            
            data = {"name":"case1","age":12,"gender":"F", "diagnosis":"testing", "system": sysId}
            url = reverse("case-create")
            request = factory.post(url, data, format='json')
            force_authenticate(request, user=user)
            response = view(request)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Case.objects.count(), cnt+2)
            cnt +=1
            #id = sysID is VERY hacky logic, i explot the fact that this is the second time a case is created, thats all
            self.assertEqual(list(map(lambda x: x.finding.id , Case.objects.get(id = sysId+2).caseres_set.all())), res)

    #test delete cases
    def test_del_cases(self):
        factory = APIRequestFactory()
        view = views.caseDelete
        create_context()
        user = User.objects.get(username='foo') 
        url = reverse("case-delete", args = ["2"])
        request = factory.delete(url)
        force_authenticate(request, user=user)
        response = view(request,"2")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        request = factory.get(reverse("case-list"))
        view = views.caseList
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data,[OrderedDict([('id', 1), ('system', OrderedDict([('name', 'system1'), ('id', 1)])), ('name', 'case1'), ('gender', 'F'), ('age', 34), ('diagnosis', 'not important'), ('findings', [1, 4])])])

    #edit individual caseres

    def test_caseRes_update(self):
        factory = APIRequestFactory()
        view = views.caseResUpdate
        create_context()
        #user = User.objects.get(username='foo') 
        data = {"case":1, "finding":2}
        url = reverse("case-res-update", args = ["1"])
        request = factory.patch(url, data, format='json')
        #force_authenticate(request, user=user)
        response = view(request,"1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'case': 1, 'finding': 2})

        



