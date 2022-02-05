from django.contrib import admin
from .models import *

try:
    admin.site.register(Account)
except:
    pass

try:
    admin.site.register(Transaction)
except:
    pass
