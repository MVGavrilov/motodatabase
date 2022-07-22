from django.contrib import admin

from .models import *


class MotorcycleFeaturesInline(admin.StackedInline):
    model = MotorcycleFeature
    extra = 0


class MotorcycleAdmin(admin.ModelAdmin):
    inlines = [MotorcycleFeaturesInline]


admin.site.register(Manufacturer)
admin.site.register(Model)
admin.site.register(Motorcycle, MotorcycleAdmin)
admin.site.register(MotorcycleFeature)
