from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import * 

# User Admin
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'name', 'email', 'is_active')
    fieldsets = (
        ('General Info', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'name', 'photo','bio', 'url','location')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', )
    filter_horizontal = ()




# Feedback Admin
class FeedbackAdmin(BaseUserAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('name', 'email', 'subject', 'created_at')
    fieldsets = (
        ('Personal Info', {'fields': ('name', 'email')}),
        ('Feedback Info', {'fields': ('subject', 'message')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'subject', 'created_at')
        }),
    )
    search_fields = ('name', 'email', 'subject', 'created_at')
    ordering = ('created_at',)
    filter_horizontal = ()
     
# set user admin
admin.site.register(User, UserAdmin)

# set feedback admin
admin.site.register(Feedback, FeedbackAdmin)

# set subscribe admin
admin.site.register(Subscribe)