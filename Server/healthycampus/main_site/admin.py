from django.contrib import admin
from main_site.models import Page

class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['header', 'content', 'footer']}),
    ]
    #list_display = ('question_text', 'pub_date', 'was_published_recently')
    #list_filter = ['pub_date']
    search_fields = ['header']

admin.site.register(Page, PageAdmin)