from django.contrib import admin
from .models import Location,Mechanic,RepairRequest,ProblemSubmission
admin.site.register(Mechanic)
admin.site.register(ProblemSubmission)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['user', 'url', 'timestamp']

@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ['requested_by', 'mechanic', 'status', 'location', 'created_at']

#to show admin mechanic details to call for interview
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'mobile_number', 'address']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile_number', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

