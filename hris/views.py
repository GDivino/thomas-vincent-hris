from distutils.command.build_scripts import first_line_re
import os
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import UserT, WorkerT, ProjectT, AssignmentT, EvaluationReportT

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
    return render(request, 'hris/projects/view_project.html', {'project': project_details})


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
    return render(request, 'hris/workers/worker_details.html', {'worker': worker})

def delete_worker(request, pk):
    worker = get_object_or_404(WorkerT, pk=pk)

    if worker.image:
        worker_img = worker.image.path
        if os.path.exists(worker_img):
            os.remove(worker_img)
    
    WorkerT.objects.filter(pk=pk).delete()
    return redirect('workers')

def update_worker(request, pk):
    if request.method == 'POST':
        ffirst_name = request.POST.get('first_name')
        flast_name = request.POST.get('last_name')
        fcontact_number = request.POST.get('contact')
        fimage = request.FILES.get('image')

        worker = get_object_or_404(WorkerT, pk=pk)

        if fimage == None:
            fimage = worker.image
        else:
            if worker.image:
                os.remove(worker.image.path)

            worker_details = WorkerT.objects.get(pk=pk)
            worker_details.image = fimage
            worker_details.save()
        
        WorkerT.objects.filter(pk=pk).update(first_name=ffirst_name, last_name=flast_name, contact_number=fcontact_number)
        worker = get_object_or_404(WorkerT, pk=pk)
        # return render(request, 'hris/workers/update_worker.html', {'worker': worker})
        return redirect('worker_details', pk=pk)
    else:
        worker = get_object_or_404(WorkerT, pk=pk)
        return render(request, 'hris/workers/update_worker.html', {'worker': worker})