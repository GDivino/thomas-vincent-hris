import os
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import UserT, WorkerT, ProjectT, AssignmentT, EvaluationReportT
from django.contrib.sessions.models import Session

Session.objects.all().delete()

# helper functions
def imageUpdate(upload, existing, db, pk):
    if upload == None: # if no file upload
            upload = existing
    else: # if there's a file upload
        if existing: # if file exists already
            os.remove(existing.path)

        worker_details = db.objects.get(pk=pk)
        worker_details.image = upload
        worker_details.save()

def bioDataUpdate(upload, existing, db, pk):
    if upload == None: # if no file upload
            upload = existing
    else: # if there's a file upload
        if existing: # if file exists already
            os.remove(existing.path)

        worker_details = db.objects.get(pk=pk)
        worker_details.biodata = upload
        worker_details.save()

def signedContractUpdate(upload, existing, db, pk):
    if upload == None: # if no file upload
            upload = existing
    else: # if there's a file upload
        if existing: # if file exists already
            os.remove(existing.path)

        worker_details = db.objects.get(pk=pk)
        worker_details.contract = upload
        worker_details.save()

def nbiClearanceUpdate(upload, existing, db, pk):
    if upload == None: # if no file upload
            upload = existing
    else: # if there's a file upload
        if existing: # if file exists already
            os.remove(existing.path)

        worker_details = db.objects.get(pk=pk)
        worker_details.nbi_clearance = upload
        worker_details.save()

def medicalReportUpdate(upload, existing, db, pk):
    if upload == None: # if no file upload
            upload = existing
    else: # if there's a file upload
        if existing: # if file exists already
            os.remove(existing.path)

        worker_details = db.objects.get(pk=pk)
        worker_details.medical_report = upload
        worker_details.save()

def fileCheckDelete(file):
    if file:
        path = file.path
        if os.path.exists(path):
            os.remove(path)

def auth(req):
    if req.session.get('authenticated'):
        return req.session['authenticated']
    return False

def redirect_home(request):
    return redirect('workers')


# Projects Page
def projects(request):
    user = auth(request)
    if user == False:
        return redirect('login')

    project_objects = ProjectT.objects.all()
    return render(request, 'hris/projects/projects.html', {'projects':project_objects, 'user': user})

def add_project(request):
    user = auth(request)
    if user == False:
        return redirect('login')

    if(request.method=='POST'):
        ptitle = request.POST.get('ptitle')
        pstatus = request.POST.get('pstatus')
        ptype = request.POST.get('ptype')
        plocation = request.POST.get('plocation')
        pclient = request.POST.get('pclient')
        pclientcontact = request.POST.get('pclientcontact')
        ppic = request.POST.get('ppic')
        ppiccontact = request.POST.get('ppiccontact')
        pstartdate = request.POST.get('pstartdate')
        penddate = request.POST.get('penddate')

        ProjectT.objects.create(project_title=ptitle, status=pstatus, project_type=ptype, project_location=plocation, client=pclient, client_contact_number=pclientcontact, project_in_charge=ppic, project_in_charge_contact_number=ppiccontact, start_date=pstartdate, end_date=penddate)
        return redirect('projects')
    else:
        return render(request, 'hris/projects/add_project.html', {'user': user})

def view_project_details(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')
    
    project_details = get_object_or_404(ProjectT, pk=pk)
    worker_objects = WorkerT.objects.all()
    assigned = AssignmentT.objects.filter(project_id=pk).all()
    return render(request, 'hris/projects/view_project.html', {'project': project_details, 'workers': worker_objects, 'assigned':assigned, 'user': user})

def update_project(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    project_details = get_object_or_404(ProjectT, pk=pk)

    if(request.method=='POST'):
        ptitle = request.POST.get('ptitle')
        pstatus = request.POST.get('pstatus')
        ptype = request.POST.get('ptype')
        plocation = request.POST.get('plocation')
        pclient = request.POST.get('pclient')
        pclientcontact = request.POST.get('pclientcontact')
        ppic = request.POST.get('ppic')
        ppiccontact = request.POST.get('ppiccontact')
        pstartdate = request.POST.get('pstartdate')
        penddate = request.POST.get('penddate')

        if penddate == '':
            penddate = project_details.end_date
        
        if pstartdate == '':
            pstartdate = project_details.start_date

        ProjectT.objects.filter(pk=pk).update(project_title=ptitle, status=pstatus, project_type=ptype, project_location=plocation, client=pclient, client_contact_number=pclientcontact, project_in_charge=ppic, project_in_charge_contact_number=ppiccontact, start_date=pstartdate, end_date=penddate)
        return redirect('view_project_details', pk=pk)

    project_details.start_date = str(project_details.start_date)
    project_details.end_date = str(project_details.end_date)

    return render(request, 'hris/projects/update_project.html', {'project': project_details, 'user': user})


# Workers Page
def workers(request):
    user = auth(request)
    if user == False:
        return redirect('login')

    worker_objects = WorkerT.objects.all()
    return render(request, 'hris/workers/workers.html', {'workers': worker_objects, 'user': user})

def add_worker(request):
    user = auth(request)
    if user == False:
        return redirect('login')

    if request.method == 'POST':
        ffirst_name = request.POST.get('first_name')
        flast_name = request.POST.get('last_name')
        fcontact_number = request.POST.get('contact')
        fimage = request.FILES.get('image')
        fbiodata = request.FILES.get('biodata')

        WorkerT.objects.create(first_name=ffirst_name, last_name=flast_name, contact_number=fcontact_number, image=fimage, biodata=fbiodata)
        return redirect('workers')
    else:
        return render(request, 'hris/workers/add_worker.html', {'user': user})

def worker_details(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    worker = get_object_or_404(WorkerT, pk=pk)
    projects = AssignmentT.objects.filter(worker_id=pk).all()
    return render(request, 'hris/workers/worker_details.html', {'worker': worker, 'projects': projects, 'user': user})

def delete_worker(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    worker = get_object_or_404(WorkerT, pk=pk)

    fileCheckDelete(worker.image)
    
    WorkerT.objects.filter(pk=pk).delete()
    return redirect('workers')

def update_worker(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    worker = get_object_or_404(WorkerT, pk=pk)
    if request.method == 'POST':
        ffirst_name = request.POST.get('first_name')
        flast_name = request.POST.get('last_name')
        fcontact_number = request.POST.get('contact')
        fimage = request.FILES.get('image')
        fbiodata = request.FILES.get('biodata')

        imageUpdate(fimage, worker.image, WorkerT, pk)
        bioDataUpdate(fbiodata, worker.biodata, WorkerT, pk)
        
        WorkerT.objects.filter(pk=pk).update(first_name=ffirst_name, last_name=flast_name, contact_number=fcontact_number)
        return redirect('worker_details', pk=pk)

    return render(request, 'hris/workers/update_worker.html', {'worker': worker, 'user': user})


# Applicant Feature
def add_applicant(request, project_pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    if request.method == 'POST':
        fworker_id = request.POST.get('wWorkerId')
        fposition = request.POST.get('wRole')
        fstart_date = request.POST.get('wStartDate')
        fend_date = request.POST.get('wEndDate')
        fbase_pay = request.POST.get('wBasePay')
        fsigned_contract = request.FILES.get('wSignedContract')
        fnbi_clearance = request.FILES.get('wNbiClearance')
        fmedical_report = request.FILES.get('wMedicalReport')

        worker = WorkerT.objects.get(worker_id=fworker_id)
        project = ProjectT.objects.get(project_id=project_pk)

        if AssignmentT.objects.filter(worker_id=fworker_id, project_id=project_pk).exists() == True:
            messages.error(request, 'Applicant already exists')
        else:
            AssignmentT.objects.create(worker_id=fworker_id, project_id=project_pk, role=fposition, base_pay=fbase_pay, start_date=fstart_date, end_date=fend_date, medical_report=fmedical_report, nbi_clearance=fnbi_clearance, contract=fsigned_contract, aworker=worker, aproject=project)
            return redirect('view_project_details', pk=project_pk)

    return redirect('view_project_details', pk=project_pk)

def view_applicant(request, pk):
    eval = None

    user = auth(request)
    if user == False:
        return redirect('login')

    applicant = get_object_or_404(AssignmentT, pk=pk)

    if EvaluationReportT.objects.filter(eassignment=pk).exists():
        eval = EvaluationReportT.objects.get(eassignment=pk)
    
    return render(request, 'hris/applicants/view_applicant.html', {'applicant':applicant, 'user': user, 'eval': eval})

def update_applicant(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    applicant = get_object_or_404(AssignmentT, pk=pk)
    workers = WorkerT.objects.all()

    if request.method == 'POST':
        fworker_id = request.POST.get('wWorkerId')
        fposition = request.POST.get('role')
        fstart_date = request.POST.get('start-date')
        fend_date = request.POST.get('end-date')
        fbase_pay = request.POST.get('wBasePay')
        fsigned_contract = request.FILES.get('wSignedContract')
        fnbi_clearance = request.FILES.get('wNbiClearance')
        fmedical_report = request.FILES.get('wMedicalReport')

        signedContractUpdate(fsigned_contract, applicant.contract, AssignmentT, pk)
        nbiClearanceUpdate(fnbi_clearance, applicant.nbi_clearance, AssignmentT, pk)
        medicalReportUpdate(fmedical_report, applicant.medical_report, AssignmentT, pk)

        if fstart_date == '':
            fstart_date = applicant.start_date
        
        if fend_date == '':
            fend_date = applicant.end_date

        AssignmentT.objects.filter(pk=pk).update(worker_id=fworker_id, role=fposition, start_date=fstart_date, end_date=fend_date, base_pay=fbase_pay, medical_report=fmedical_report, nbi_clearance=fnbi_clearance, contract=fsigned_contract)
        return redirect('view_applicant', pk=pk)
    
    applicant.start_date = str(applicant.start_date)
    applicant.end_date = str(applicant.end_date)
    
    return render(request, 'hris/applicants/update_applicant.html', {'applicant':applicant, 'workers':workers, 'user': user})

def unassign_applicant(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    applicant = get_object_or_404(AssignmentT, pk=pk)

    fileCheckDelete(applicant.contract)
    fileCheckDelete(applicant.nbi_clearance)
    fileCheckDelete(applicant.medical_report)

    AssignmentT.objects.filter(pk=pk).delete()
    return redirect('view_project_details', pk=applicant.project_id)

def add_eval(request, applicant_pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    worker = AssignmentT.objects.get(assignment_id=applicant_pk)

    if request.method == 'POST':
        worker_strength = request.POST.get('worker_strength')
        aoi = request.POST.get('aoi')
        poa = request.POST.get('poa')
        kow = request.POST.get('kow')
        attendance = request.POST.get('attendance')
        voo = request.POST.get('voo')
        attitude = request.POST.get('attitude')
        eassignment = worker
        overall_rating = (int(kow) + int(attendance) + int(voo) + int(attitude)) / 4

        EvaluationReportT.objects.create(overall_rating=overall_rating, worker_strength=worker_strength, areas_of_improvement=aoi, plan_of_action=poa, knowledge_of_work=kow, attendance=attendance, volume_of_output=voo, attitude=attitude, eassignment=eassignment)

        return redirect('view_applicant', pk=applicant_pk)
    
    if EvaluationReportT.objects.filter(eassignment=applicant_pk).exists():
        return redirect('view_applicant', pk=applicant_pk)

    return render(request, 'hris/applicants/add_eval.html', {'user': user, 'worker': worker})

def update_eval(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')
    
    eval = EvaluationReportT.objects.get(eval_id=pk)
    
    if request.method == 'POST':
        worker_strength = request.POST.get('worker_strength')
        aoi = request.POST.get('aoi')
        poa = request.POST.get('poa')
        kow = request.POST.get('kow')
        attendance = request.POST.get('attendance')
        voo = request.POST.get('voo')
        attitude = request.POST.get('attitude')
        overall_rating = (int(kow) + int(attendance) + int(voo) + int(attitude)) / 4
    
        EvaluationReportT.objects.filter(eval_id=pk).update(overall_rating=overall_rating, worker_strength=worker_strength, areas_of_improvement=aoi, plan_of_action=poa, knowledge_of_work=kow, attendance=attendance, volume_of_output=voo, attitude=attitude)
        print(eval.eassignment.assignment_id)

        return redirect('view_applicant', pk=eval.eassignment.assignment_id)
    
    return render(request, 'hris/applicants/update_eval.html', {'eval': eval})


# User function
def users(request):
    user = auth(request)
    if user == False:
        return redirect('login')

    users_objects = UserT.objects.all()
    return render(request, 'hris/users/users.html', {'users':users_objects, 'user': user})

def add_users(request):
    user = auth(request)
    if user == False:
        return redirect('login')

    if request.method=='POST':
        uformalname = request.POST.get('uformalname')
        u_type = request.POST.get('u_type')
        u_username = request.POST.get('u_username')
        u_password = make_password(request.POST.get('u_password'))

        if UserT.objects.filter(username=u_username).exists():
            return redirect('add_users')

        UserT.objects.create(name=uformalname, user_type=u_type, username=u_username, password=u_password)
        return redirect('users')

    else:
        return render(request, 'hris/users/add_users.html', {'user': user})

def update_user(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')
    
    user_edit = UserT.objects.get(user_id=pk)

    if request.method == 'POST':
        uformalname = request.POST.get('uformalname')
        u_type = request.POST.get('u_type')
        u_username = request.POST.get('u_username')
        u_current_pass = request.POST.get('u_current_pass')
        u_password = make_password(request.POST.get('u_password'))

        if u_current_pass == '':
            UserT.objects.filter(user_id=pk).update(name=uformalname,user_type=u_type, username=u_username)
            return redirect('users')

        if check_password(u_current_pass, user_edit.password):
            UserT.objects.filter(user_id=pk).update(name=uformalname, user_type=u_type, username=u_username, password=u_password)
            return redirect('users')
    
    return render(request, 'hris/users/update_user.html', {'user': user, 'curr_user': user_edit})

def delete_user(request, pk):
    user = auth(request)
    if user == False:
        return redirect('login')

    UserT.objects.filter(user_id=pk).delete()
    return redirect('users')

def login(request):
    if request.method == 'POST':        
        uname = request.POST.get('uname')
        pw = request.POST.get('pw')

        if UserT.objects.filter(username=uname).exists():
            user = UserT.objects.get(username=uname)

        if UserT.objects.filter(username=uname).exists() and check_password(pw, user.password):
            request.session['authenticated'] = uname
            return redirect('workers')
    
    return render(request, 'hris/users/login.html')

def logout(request):
    try: 
        del request.session['authenticated']
    except:
        pass

    return redirect('login')