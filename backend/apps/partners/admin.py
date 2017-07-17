from django.contrib import admin
from apps.partners.models import Partner, Worker
# Register your models here.


class WorkerInline(admin.StackedInline):
    model = Worker

class PartnerAdmin(admin.ModelAdmin):
    inlines = (WorkerInline, )

admin.site.register(Partner, PartnerAdmin)
admin.site.register(Worker)
