from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from uploads.core.models import Json, Yaml ,Name
from uploads.core.forms import JsonForm , NameForm, YamlForm
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render 
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
import urllib.parse as urlparse
from urllib.parse import parse_qs
from deepdiff import DeepDiff
import os
import glob
import filecmp
import json
import re

def home(request):
    return render(request, 'core/home.html')

path_sec = 'media\\documents\\'
path_na = 'media\\'

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file = fs.url(filename)
        uploaded_file_url = uploaded_file.replace("/", "\\")[1:]

        if uploaded_file_url.endswith('.json'):
            type_name = "json"

        elif uploaded_file_url.endswith('.yml'):
            type_name = "yml"

        else:
            noto = "Plz upload yml or json file"
            return render(request, 'core/compare.html', {
                'noto' : noto
        } )

        list_of_files = glob.glob(path_sec+ type_name +"\\*"+type_name)
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            f2 = f.read()
        with open(uploaded_file_url, 'r') as f:
            f1 = f.read()
            l1 = f1.split('\n')
        
        A = DeepDiff(f1, f2)
        A["values_changed"]["root"]["new_value"] = A["values_changed"]["root"]["new_value"].replace("\n",'')
        A["values_changed"]["root"]["old_value"] = A["values_changed"]["root"]["old_value"].replace("\n",'')
        A["values_changed"]["root"]["diff"] = A["values_changed"]["root"]["diff"].replace("\n",'')
        D = A["values_changed"]["root"]["diff"]
        
        Line_no = (re.findall(r"@@ -(\d+)", D))
        
        for i in range(0, len(Line_no)): 
            Line_no[i] = int(Line_no[i])
        for i in range(len(Line_no)):
            Line_no[i] += 2
        NewList = [l1[x] for x in Line_no]
        for i in range(len(Line_no)):
            Line_no[i] += 1
        res = list(zip(Line_no, NewList))

        list_na = glob.glob(path_na+"\\*"+type_name)
        latest_na = max(list_na, key=os.path.getctime)
        os.remove(latest_na)

        return render(request, 'core/compare.html', {
                'res':res,
                'type_name':type_name
        } )
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    test = str(request.get_full_path)
    o = urlparse.urlsplit(test)
    foo = o.query
    var = foo.replace(' ', '')[:-3]
    if var == "json" :
        if request.method == 'POST':
            form = JsonForm(request.POST, request.FILES)
            if form.is_valid():
               form.save()
               return HttpResponseRedirect('home')
            else:
               form = JsonForm()
    elif var == "yaml" :
        if request.method == 'POST':
            form = YamlForm(request.POST, request.FILES)
            if form.is_valid():
               form.save()
               return HttpResponseRedirect("home")
            else:
               form = YamlForm()   
    return render(request, 'core/model_form_upload.html', {
        'form':form,
    })

def add_tech(request):
    return render(request, 'core/add_tech.html')


def upload_type(request):
    if request.method =='POST':   
        details = NameForm(request.POST) 
        if details.is_valid():
            return render(request,"core/upload_type.html",{'test': details})  
    else:
        details = NameForm()

    return render(request, 'core/upload_type.html', {'test': details})
