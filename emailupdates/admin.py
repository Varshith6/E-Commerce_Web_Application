from django.contrib import admin
from emailupdates.models import Emailupdate


# Register your models here.
class EmailAdmin(admin.ModelAdmin):
    list_display = ('Email','date_added',)

admin.site.register(Emailupdate,EmailAdmin)
