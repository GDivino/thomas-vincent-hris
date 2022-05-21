from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import UserT
# admin.site.register(UserT)

class UserTForm(forms.ModelForm):
    class Meta:
        model = UserT
        fields = '__all__'
    def clean_password(self):        
        return make_password(self.cleaned_data['password'])

@admin.register(UserT)
class UserT(admin.ModelAdmin):
    form = UserTForm

from .models import WorkerT
admin.site.register(WorkerT)

from .models import ProjectT
admin.site.register(ProjectT)

from .models import EvaluationReportT
admin.site.register(EvaluationReportT)

from .models import AssignmentT
admin.site.register(AssignmentT)
