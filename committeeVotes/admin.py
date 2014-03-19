from django.contrib import admin
from committeeVotes.models import Bill, VoteType, Minister, Meeting, Vote


#class VoteAdmin(admin.ModelAdmin):
#    def formfield_for_manytomany(self, db_field, request, **kwargs):
#        if db_field.name == "meeting":
#            kwargs["queryset"] = Meeting.objects.filter(proposed_bills)
#        return super(VoteAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Bill)
admin.site.register(VoteType)
admin.site.register(Minister)
admin.site.register(Meeting)
admin.site.register(Vote)#, VoteAdmin)


