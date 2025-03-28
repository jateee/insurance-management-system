from django.contrib import admin

#Override default admin site
admin.site.site_header = 'FEDHA INSURANCE MANAGEMENT SYSTEM'  # This will change the top header text.
admin.site.site_title = 'Administration Portal'  # This will change the browser title (in the tab).
admin.site.index_title = 'Welcome to Fedha Administration site '  # This will change the index page title.


from .models import Claim
from .models import Policy


class ClaimAdmin(admin.ModelAdmin):
    list_display = ('policy', 'claim_amount', 'status', 'date_submitted')
    list_filter = ('status',)
    search_fields = ('date_submitted', 'status',)

admin.site.register(Claim, ClaimAdmin)


class PolicyAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_policy_type_display', 'policy_number', 'start_date', 'end_date')
    list_filter = ('policy_type',)
    search_fields = ('policy_type', 'policy_number',)
    ordering = ('-start_date',)

admin.site.register(Policy, PolicyAdmin)



# Register your models here.
