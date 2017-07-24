import zipfile
import os

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.files.base import File

from .models import Contest,Problem
from .forms import ProblemText
from userprof.models import UserProfile



id_error=""
title_error=""
file_error=""

def validate_form(request):
    global id_error
    global title_error
    global file_error

    try:
        prob_obj1 = Problem.objects.get(problem_id=request.POST.get('problem_id'))
    except:
        prob_obj1 = None

    try:
        prob_obj2 = Problem.objects.get(name_of_problem=request.POST.get('problem_title'))
    except:
        prob_obj2 = None

    if prob_obj1 is not None:
        id_error = "This problem id already exists"
    if prob_obj2 is not None:
        title_error = "This problem title already exists"
    if (zipfile.is_zipfile(request.FILES['test_files'])) == False:
        file_error = "Uploaded Filetype is not zip"

    if ((prob_obj1 is  None) and (prob_obj2 is  None) and 
        ((zipfile.is_zipfile(request.FILES['test_files'])) == True)):
        return True

    return False


def contest_view(request,contest_id):
    user_obj = UserProfile.objects.get(user=request.user)
    contest_obj = Contest.objects.get(contest_id=contest_id)
    all_problems = contest_obj.problems.all
    return render(request,'contest/contest_view.html',
        {'contest_obj':contest_obj,'all_problems':all_problems,'user_obj':user_obj,})
    


def prob_upload(request):
    global id_error
    global title_error
    global file_error

    submitted = None
    all_contests = Contest.objects.all
    problem_obj = Problem()
    form  = ProblemText()

    if request.method == "POST":
        contest_obj = Contest.objects.get(name_of_contest=request.POST.get('contest_dropdown'))
        zipped_file = request.FILES['test_files']

        if validate_form(request)==True:


            submitted = True
            problem_obj = Problem(problem_id=request.POST.get('problem_id'),
                                  name_of_problem=request.POST.get('problem_title'),
                                  max_score=request.POST.get('max_score'),
                                  time_limit=request.POST.get('time_limit'),
                                  contest=contest_obj,
                                  test_files=zipped_file,
                                  statement=request.POST.get('statement'),
                                  )
            problem_obj.save()
            unzipped_file = zipfile.ZipFile(zipped_file)
            p_id = request.POST.get('problem_id')    
            i=0
            path_to_save = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path_to_save = os.path.join(path_to_save,'media/problems/problem_'+str(p_id))
            print path_to_save
            print "save_dir " +os.path.join(path_to_save,'input')
            os.makedirs( os.path.join(path_to_save,'input'),0755)
            os.makedirs( os.path.join(path_to_save,'output'),0755)

            for item in unzipped_file.namelist():
                if i<=4:
                    file_ = file(path_to_save+'/input/input0'+str(i)+'.txt','w').write(unzipped_file.read(item))
                else:
                    file_ = file(path_to_save+'/output/output0'+str(i-5)+'.txt','w').write(unzipped_file.read(item))

                i+=1
        else:
            submitted = False



    return render(request,'contest/problem_view.html',{'all_contests':all_contests,
                                                        'submitted':submitted,
                                                        'id_error':id_error,
                                                        'title_error':title_error,
                                                        'file_error':file_error,
                                                        'problem_obj':problem_obj,
                                                        'form':form,
                                                        }) 


def problem_view(request,problem_id):
    problem_obj = Problem.objects.get(problem_id=problem_id)

    return render(request,'contest/problem_statement.html',{'problem_obj':problem_obj})



