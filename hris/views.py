from distutils.command.build_scripts import first_line_re
import os
from time import strftime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import UserT, WorkerT, ProjectT, AssignmentT, EvaluationReportT

# helper functions
def fileCheckUpload(upload, existing, db, pk):
    if upload == None: # if no file upload
            upload = existing
    else: # if there's a file upload
        if existing: # if file exists already
            os.remove(existing.path)

        worker_details = db.objects.get(pk=pk)
        worker_details.image = upload
        worker_details.save()

def fileCheckDelete(file):
    if file:
        path = file.path
        if os.path.exists(path):
            os.remove(path)


def dashboard(request):
    return render(request, 'hris/dashboard.html')

# Projects Page
def projects(request):
    project_objects = ProjectT.objects.all()
    return render(request, 'hris/projects/projects.html', {'projects':project_objects})

def add_project(request):
    if(request.method=='POST'):
        ptitle = request.POST.get('ptitle')
        ptype = request.POST.get('ptype')
        plocation = request.POST.get('plocation')
        pclient = request.POST.get('pclient')
        pclientcontact = request.POST.get('pclientcontact')
        ppic = request.POST.get('ppic')
        ppiccontact = request.POST.get('ppiccontact')
        pstartdate = request.POST.get('pstartdate')
        penddate = request.POST.get('penddate')

        ProjectT.objects.create(project_title=ptitle, project_type=ptype, project_location=plocation, client=pclient, client_contact_number=pclientcontact, project_in_charge=ppic, project_in_charge_contact_number=ppiccontact, start_date=pstartdate, end_date=penddate)
        return redirect('projects')
    else:
        return render(request, 'hris/projects/add_project.html')

def view_project_details(request, pk):
    project_details = get_object_or_404(ProjectT, pk=pk)
    worker_objects = WorkerT.objects.all()
    assigned = AssignmentT.objects.filter(project_id=pk).all()
    return render(request, 'hris/projects/view_project.html', {'project': project_details, 'workers': worker_objects, 'assigned':assigned})

def update_project(request, pk):
    project_details = get_object_or_404(ProjectT, pk=pk)

    if(request.method=='POST'):
        ptitle = request.POST.get('ptitle')
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

        ProjectT.objects.filter(pk=pk).update(project_title=ptitle, project_type=ptype, project_location=plocation, client=pclient, client_contact_number=pclientcontact, project_in_charge=ppic, project_in_charge_contact_number=ppiccontact, start_date=pstartdate, end_date=penddate)
        return redirect('view_project_details', pk=pk)

    project_details.start_date = str(project_details.start_date)
    project_details.end_date = str(project_details.end_date)

    return render(request, 'hris/projects/update_project.html', {'project': project_details})


# Workers Page
def workers(request):
    worker_objects = WorkerT.objects.all()
    return render(request, 'hris/workers/workers.html', {'workers': worker_objects})

def add_worker(request):
    if request.method == 'POST':
        ffirst_name = request.POST.get('first_name')
        flast_name = request.POST.get('last_name')
        fcontact_number = request.POST.get('contact')
        fimage = request.FILES.get('image')

        WorkerT.objects.create(first_name=ffirst_name, last_name=flast_name, contact_number=fcontact_number, image=fimage)
        return redirect('workers')
    else:
        return render(request, 'hris/workers/add_worker.html')

def worker_details(request, pk):
    worker = get_object_or_404(WorkerT, pk=pk)
    projects = AssignmentT.objects.filter(worker_id=pk).all()
    return render(request, 'hris/workers/worker_details.html', {'worker': worker, 'projects': projects})

def delete_worker(request, pk):
    worker = get_object_or_404(WorkerT, pk=pk)

    fileCheckDelete(worker.image)
    
    WorkerT.objects.filter(pk=pk).delete()
    return redirect('workers')

def update_worker(request, pk):
    worker = get_object_or_404(WorkerT, pk=pk)
    if request.method == 'POST':
        ffirst_name = request.POST.get('first_name')
        flast_name = request.POST.get('last_name')
        fcontact_number = request.POST.get('contact')
        fimage = request.FILES.get('image')

        fileCheckUpload(fimage, worker.image, WorkerT, pk)
        
        WorkerT.objects.filter(pk=pk).update(first_name=ffirst_name, last_name=flast_name, contact_number=fcontact_number)
        return redirect('worker_details', pk=pk)

    return render(request, 'hris/workers/update_worker.html', {'worker': worker})


# Applicant Feature
def add_applicant(request, project_pk):
    if request.method == 'POST':
        fworker_id = request.POST.get('wWorkerId')
        fposition = request.POST.get('wPosition')
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
    applicant = get_object_or_404(AssignmentT, pk=pk)
    return render(request, 'hris/applicants/view_applicant.html', {'applicant':applicant})

def update_applicant(request, pk):
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

        fileCheckUpload(fsigned_contract, applicant.contract, AssignmentT, pk)
        fileCheckUpload(fnbi_clearance, applicant.nbi_clearance, AssignmentT, pk)
        fileCheckUpload(fmedical_report, applicant.medical_report, AssignmentT, pk)

        if fstart_date == '':
            fstart_date = applicant.start_date
        
        if fend_date == '':
            fend_date = applicant.end_date

        AssignmentT.objects.filter(pk=pk).update(worker_id=fworker_id, role=fposition, start_date=fstart_date, end_date=fend_date, base_pay=fbase_pay, medical_report=fmedical_report, nbi_clearance=fnbi_clearance, contract=fsigned_contract)
        return redirect('view_applicant', pk=pk)
    
    applicant.start_date = str(applicant.start_date)
    applicant.end_date = str(applicant.end_date)
    
    return render(request, 'hris/applicants/update_applicant.html', {'applicant':applicant, 'workers':workers})

def unassign_applicant(request, pk):
    applicant = get_object_or_404(AssignmentT, pk=pk)

    fileCheckDelete(applicant.contract)
    fileCheckDelete(applicant.nbi_clearance)
    fileCheckDelete(applicant.medical_report)

    AssignmentT.objects.filter(pk=pk).delete()
    return redirect('view_project_details', pk=applicant.project_id)