from django.contrib import admin

from .models import Worker

class WorkerAdmin(admin.ModelAdmin):
    list = ('worker_name',
'worker_age',
'working_job',
'working_duration',
'worker_phone',
'worker_payment',
'worker_address', 
'worker_image')
    
admin.site.register(Worker,WorkerAdmin)
