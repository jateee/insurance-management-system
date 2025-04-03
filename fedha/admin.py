from django.contrib import admin

# Override default admin site
admin.site.site_header = 'FEDHA INSURANCE MANAGEMENT SYSTEM'  # Changes the top header text.
admin.site.site_title = 'Administration Portal'  # Changes the browser tab title.
admin.site.index_title = 'Welcome to Fedha Administration site'  # Changes the index page title.

# Import your models
from .models import Claim
from .models import Policy
from .models import ContactMessage

# Claim Admin
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('policy', 'claim_amount', 'status', 'date_submitted')
    list_filter = ('status',)
    search_fields = ('date_submitted', 'status',)

admin.site.register(Claim, ClaimAdmin)

# Policy Admin
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_policy_type_display', 'policy_number', 'start_date', 'end_date')
    list_filter = ('policy_type',)
    search_fields = ('policy_type', 'policy_number',)
    ordering = ('-start_date',)

admin.site.register(Policy, PolicyAdmin)




@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')  # Fields to display in the admin
    search_fields = ('name', 'email', 'message')  # Searchable fields in the admin panel