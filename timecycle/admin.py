from django.contrib import admin

from .models import Day, MetaCycle, Activity  # Import your Day model

admin.site.register(Day)  # Register the Day model
admin.site.register(MetaCycle)
admin.site.register(Activity)