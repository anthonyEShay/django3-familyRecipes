from django.contrib import admin

# Register your models here.

from .models import UserProfile, UserComment

class UserCommentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )

admin.site.register(UserProfile)
admin.site.register(UserComment, UserCommentAdmin)