from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile, Follow, Post, Comment

admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Comment)
"""class PortfAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email',
                    'skills', 'gender', 'nationality')
    list_editable = ('skills',)
    list_per_page = 10
    search_fields = ('name', 'email',
                     'gender', 'skills', 'nationality')
    list_filter=('gender','skills')



# Register your models here.
admin.site.register(Portf, PortfAdmin)
admin.site.unregister(Group)"""
