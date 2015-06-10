from django.contrib import admin
from kiosk.models import Kiosk, CheckIn, User, Heartbeat, KioskDistance, UserKiosksToCheckIn

class CheckInInline(admin.TabularInline):
    model = CheckIn
    extra = 1

class HeartbeatInline(admin.TabularInline):
    model = Heartbeat
    extra = 1
    
'''class PathInline(admin.TabularInline):
    model = Path
    extra = 1'''
    
class KioskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'address', 'x', 'y']}),
        #('Last Checked In', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [CheckInInline, HeartbeatInline] #PathInLine
    search_fields = ['name', 'address']
    
#################################################################################
class UserKiosksToCheckInInLine(admin.TabularInline):
    model = UserKiosksToCheckIn
       
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        #(None,               {'fields': ['username', 'password', 'barcode']}),
    ]
    inlines = [UserKiosksToCheckInInLine]
    #list_display = ('question_text', 'pub_date', 'was_published_recently')
    #list_filter = ['pub_date']
   # search_fields = ['username', 'barcode']
    
#################################################################################  
    
'''class PathNodeInline(admin.TabularInline):
    model = PathNode
    extra = 1

class PathAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['kiosk', 'difficulty']}),
        #('Last Checked In', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [PathNodeInline]
    search_fields = ['kiosk', 'difficulty']
  '''  
#################################################################################
class KioskDistanceInline(admin.TabularInline):
    pass

class KioskDistanceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['kiosk_one', 'kiosk_two', 'distance_m']}),
        #('Last Checked In', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #inlines = [KioskDistanceInLine]
    #search_fields = ['kiosk', 'difficulty']
    
admin.site.register(User, UserAdmin)
admin.site.register(Kiosk, KioskAdmin)
#admin.site.register(Path, PathAdmin)
admin.site.register(KioskDistance, KioskDistanceAdmin)
