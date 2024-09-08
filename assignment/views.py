from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
import json
from django.http import JsonResponse
from .utils import *

# Create your views here.

def index(request):    
    return render(request,'home.html')

def getTest(request):
    if(request.method=='POST'):
        context = request.POST.get('context', '')
        screenshots = request.FILES.getlist('screenshots')    
        test_instructions = getTestLLM(context, screenshots[0])
        return render(request,'result.html', {'test_cases': test_instructions})
        # return HttpResponse("YEEEEEE succcessss")
       
    return redirect('/')

def result(request):
    pass
