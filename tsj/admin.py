from django.contrib import admin
from tsj.models import *

admin.site.register(Company)
admin.site.register(Resident)
admin.site.register(House)
admin.site.register(Street)
admin.site.register(ServiceCompany)
admin.site.register(MeterType)
admin.site.register(MeterReadingHistory)