import os
import subprocess
import shlex

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

from .models import SolutionCode
from contest.models import Problem
from userprof.models import UserProfile


def checker(request,problem_obj,solution_obj):

    verdict = {1:"Accepted",2:"Wrong answer",3:"Time Limit Exceeded",
                4:"Compilation Error",}


    input_dir_path = os.path.dirname(os.path.dirname(__file__))
    input_dir_path = os.path.join(input_dir_path,
        'media/problems/problem_{0}/input'.format(problem_obj.problem_id))
    all_input_list = os.listdir(input_dir_path)
    all_input_list.sort()
    
    # check for compilation error
    sol_dir_path = os.path.dirname(os.path.dirname(__file__))
    sol_dir_path = os.path.join(sol_dir_path,
        'media/solutions/user_{0}'.format(request.user.username))

    
    compile_proc = subprocess.Popen(shlex.split('g++ sol_{0}_{1}.cpp -o sol_{0}_{1}'
             .format(
                 str(problem_obj.problem_id),
                 str(solution_obj.pk))),cwd=sol_dir_path,shell=False)
    compile_proc.wait()

    all_sol_list = os.listdir(sol_dir_path)

    code_object_file = 'sol_{0}_{1}'.format(str(problem_obj.problem_id),
             str(solution_obj.pk))

    if code_object_file in all_sol_list:

        for filename in all_input_list:
            file_path = os.path.join(input_dir_path,filename)
            file_obj = open(file_path,'r')
            run_proc  = subprocess.Popen(
                        shlex.split('./'+str(code_object_file)),
                        stdin=file_obj,
                        cwd=sol_dir_path,shell=False)

            run_proc.wait() 
        
    else:
        return verdict[4]



def solution_submit(request,problem_id):
    if request.method=="POST":
        problem_obj = Problem.objects.get(problem_id=problem_id)
        user_prof = UserProfile.objects.get(user=request.user)
        solution_obj = SolutionCode(problem_associated=problem_obj,
                       user_associated=user_prof,
                       code_text=request.FILES['code_upload'],)
        code = request.FILES['code_upload'].read()
        solution_obj.save()
        
        solution_path = str(os.path.dirname(os.path.dirname(__file__)))
        extra_path = 'media/solutions/user_{0}'.format(request.user.username,)
        path_to_save = os.path.join(solution_path,extra_path)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save,0755)

        file(os.path.join(path_to_save,
            'sol_{0}_{1}.cpp'.format(str(problem_id),
             str(solution_obj.pk))),'w').write(code)
        checker(request,problem_obj,solution_obj)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))