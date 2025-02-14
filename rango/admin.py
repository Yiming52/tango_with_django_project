from django.contrib import admin
from rango.models import Category, Page, UserProfile

# Custom admin class for the Page model
class PageAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin interface
    list_display = ('title', 'category', 'url')

# Register models with the admin interface
admin.site.register(Category)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
