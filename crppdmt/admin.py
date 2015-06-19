from django.contrib import admin

import crppdmt.models

admin.site.register(crppdmt.models.Organization)
admin.site.register(crppdmt.models.Role)
admin.site.register(crppdmt.models.Person)
admin.site.register(crppdmt.models.ExpertRequest)
admin.site.register(crppdmt.models.Duty)
admin.site.register(crppdmt.models.ToR)
admin.site.register(crppdmt.models.AttendanceCode)
admin.site.register(crppdmt.models.MonthlyReport)
admin.site.register(crppdmt.models.MonthlyReportRecord)
admin.site.register(crppdmt.models.AlertType)
admin.site.register(crppdmt.models.AlertStatus)
admin.site.register(crppdmt.models.Alert)
admin.site.register(crppdmt.models.Statistic)
admin.site.register(crppdmt.models.Country)
admin.site.register(crppdmt.models.RequestStatus)
admin.site.register(crppdmt.models.ExpertProfileType)