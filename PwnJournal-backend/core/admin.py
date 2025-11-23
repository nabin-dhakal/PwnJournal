from django.contrib import admin
from .models import Writeup, UserProfile, CustomUser, Comments


admin.site.register(Writeup)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display =('user',)
    search_fields=('user__username','contact')

admin.site.register(CustomUser)
admin.site.register(Comments)