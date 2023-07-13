from django.contrib import admin

# Register your models here.
from .models import Rooms, RoomImage, Booking, Facilities
from django.utils.html import format_html

# Register your models here.

admin.site.register(Facilities)


class RoomsAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="60" style="border-radius: 10px;" />'.format(object.room_image.url))

    # thumbnail.short_description = 'Room Image'
    list_display = ('id','room_type','room_no', 'price', 'no_of_days_advance', 'start_date',  'is_available', 'get_facilities', 'thumbnail')
    # list_display_links = ('id', 'thumbnail', 'car_title')
    list_editable = ('is_available',)
    # search_fields = ('id', 'car_title', 'city', 'model', 'body_style','fuel_type')
    list_filter = ('id','room_type', 'price', 'is_available')
    
    @admin.display(description='facilities')
    def get_facilities(self, obj):
        return [facility.name for facility in obj.facilites_no.all()]
admin.site.register(Rooms, RoomsAdmin)



class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('id','room','thumbnail',)
    def thumbnail(self, object):
        return format_html('<img src="{}" width="60" style="border-radius: 10px;" />'.format(object.room_image.url))


admin.site.register(RoomImage, RoomImageAdmin)
admin.site.register(Booking)

