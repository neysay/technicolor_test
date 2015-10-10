from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.
from .models import  UserProfile



class UserInLine(admin.StackedInline):
    model = UserProfile
    list_display = ["user","city","state"]
    can_delete = False
    verbose_name_plural = 'users'

class UserAdmin(UserAdmin):
    inlines = (UserInLine, )


admin.site.unregister(User)
admin.site.register(User,UserAdmin)