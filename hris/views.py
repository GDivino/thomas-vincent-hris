from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import UserT, WorkerT, ProjectT, AssignmentT, EvaluationReportT

def dashboard(request):
    return render(request, 'hris/dashboard.html')

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