from django.contrib import admin
from .models import NewUser,Property,properties
# from django.contrib.auth.admin import UserAdmin
# from django.forms import TextInput, Textarea


# class UserAdminConfig(UserAdmin):
#     model = NewUser
#     # search_fields = ('email', 'user_name')
#     # list_filter = ('email', 'user_name',  'is_active', 'is_staff')
#     list_display = ('email', 'user_name', 
#                     'is_active', 'is_staff')
    # ordering = ('-start_date',)
    # fieldsets = (
    #     (None, {'fields': ('email', 'user_Sname',)}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
       
    # )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'user_name','password1', 'password2', 'is_active', 'is_staff')}
    #      ),
    # )


admin.site.register(NewUser)

class PropertyAdmin(admin.ModelAdmin):
    list_display=["id","name","daley_name","img1","user"]
admin.site.register(properties, PropertyAdmin)


class PropAdmin(admin.ModelAdmin):
    list_display=["name","description","img1","user"]
admin.site.register(Property,PropAdmin)
