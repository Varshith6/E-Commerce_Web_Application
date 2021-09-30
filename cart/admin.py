from django.contrib import admin
from .models import Item,OrderItem,Order,Address,Personaldetails,Payment,Contact


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'City',
        'State',
        'Pincode',
        'address_type',
        'default'
    ]
    list_filter = ['address_type','default']
    search_fields = ['user','street_address','apartment_address','Pincode']

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'txnid',
        'ordered',
        'delivered'
    ]

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Personaldetails)
admin.site.register(Payment)
admin.site.register(Contact)
