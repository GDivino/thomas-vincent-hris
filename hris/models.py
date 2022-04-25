from distutils.command.upload import upload
from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has 'on_delete' set to the desired behavior
#   * Remove 'managed = False' lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models


class AssignmentT(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    worker_id = models.IntegerField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    base_pay = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    biodata = models.TextField()
    medical_report = models.TextField(blank=True, null=True)
    nbi_clearance = models.TextField(blank=True, null=True)
    contract = models.TextField(blank=True, null=True)
    aworker = models.ForeignKey('WorkerT', models.DO_NOTHING, blank=True, null=True)
    aproject = models.ForeignKey('ProjectT', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'assignment_t'


class EvaluationReportT(models.Model):
    eval_id = models.AutoField(primary_key=True)
    overall_rating = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    worker_strength = models.CharField(max_length=180, blank=True, null=True)
    areas_of_improvement = models.CharField(max_length=180, blank=True, null=True)
    plan_of_action = models.CharField(max_length=180, blank=True, null=True)
    knowledge_of_work = models.IntegerField(blank=True, null=True)
    attendance = models.IntegerField(blank=True, null=True)
    volume_of_output = models.IntegerField(blank=True, null=True)
    attitude = models.IntegerField(blank=True, null=True)
    eassignment = models.ForeignKey(AssignmentT, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'evaluation_report_t'


class ProjectT(models.Model):
    project_id = models.AutoField(primary_key=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    project_title = models.CharField(max_length=50)
    project_type = models.CharField(max_length=30, blank=True, null=True)
    project_location = models.CharField(max_length=100, blank=True, null=True)
    client = models.CharField(max_length=50, blank=True, null=True)
    client_contact_number = models.CharField(max_length=16, blank=True, null=True)
    project_in_charge = models.CharField(max_length=50, blank=True, null=True)
    project_in_charge_contact_number = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'project_t'


class UserT(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'user_t'


class WorkerT(models.Model):
    worker_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=16, blank=True, null=True)
    image = models.ImageField(upload_to='worker')

    class Meta:
        managed = True
        db_table = 'worker_t'