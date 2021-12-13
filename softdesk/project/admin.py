from django.contrib import admin
from .managers import MyAccountManager
from .models import Users, Projects, Contributors

# Register your models here.
admin.site.register(Users)
admin.site.register(Projects)
admin.site.register(Contributors)



