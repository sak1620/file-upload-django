from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.conf import settings 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user.models import *
from user.forms import DocumentForm
from django.urls import reverse
import os
import json
from jsonschema import validate, exceptions



# Create your views here.


file_uplod_success = False



def handler404(request, *args, **kwargs):

    try:
       
        if request.user.is_active:
            return redirect(reverse("adminIndex"))
        else:
            return redirect(reverse("main_login"))

    except:
        return render(request, 'registration/login.html', status=404)


@login_required
def index(request):
    page_name = '0,side_home'
    registed_users = User.objects.all().count()
    print(registed_users,request.user.is_active)

    records = UserData.objects.all()
    print(records)

    global file_uplod_success
    fus = file_uplod_success
    file_uplod_success=False

    return render(request, "user/index.html",{"user_count":registed_users,"records":records,"records_count":len(records),"fus":fus,"page_name":page_name})



@login_required
def vw_log(request):
    logout(request)
    return render(request, 'registration/login.html')


def vw_login_user(request):
    print("login view",request.user.is_active)

    logout(request)
    username = password = ''

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse("adminIndex"))

    return render(request, 'registration/login.html')

@login_required
def file_upload(request):
    page_name = '0,side_upload'

    # Handle file upload
    error_string = ''

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = request.FILES['docfile']
            if validate_file_extension(newdoc):
                # received_file = Document(docfile = newdoc)
                # received_file.save()
                file_data = newdoc.read().decode('utf-8')
                file_des = json.loads(file_data)
                if validateJson(file_des):
                    print(len(file_des))
                  
                    objs = [
                            UserData(
                                user=User.objects.get(id=f['userId']),
                                title=f['title'],
                                body=f['body']
                            )
                            for f in file_des
                        ]
                    msg = UserData.objects.bulk_create(objs)
                    global file_uplod_success
                    file_uplod_success=True
                    return HttpResponseRedirect(reverse('adminIndex'))


                else:
                    error_string = "Not a valid Json File. Please check schema."
            else:
                error_string = "Please upload json file only."
    else:
        form = DocumentForm() # A empty, unbound form

    return render(request,
        'user/uploadfile.html',
        {'form': form,'error_string':error_string,"page_name":page_name}
        )


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    from django.forms import forms

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.json']
    if not ext.lower() in valid_extensions:
        # raise forms.ValidationError('Unsupported file extension.')
        return False
    else: 
             
        return True


def save_data_from_json(file_path):
    with open(file_path, 'r') as fp:
        data = fp.read()
        print(data)
        fp.close()

def validateJson(jsonData):
    dataSchema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "array",
        "items": [
            {
            "type": "object",
            "properties": {
                "userId": {
                "type": "integer"
                },
                "id": {
                "type": "integer"
                },
                "title": {
                "type": "string"
                },
                "body": {
                "type": "string"
                }
            },
            "required": [
                "userId",
                "id",
                "title",
                "body"
            ]
            }
        ]
        }
    try:
        validate(instance=jsonData, schema=dataSchema)
    except exceptions.ValidationError as err:
        return False
    return True
