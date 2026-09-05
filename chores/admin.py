from django.contrib import admin

from chores.models import Area, Roommate, RotationSlot, Task, TaskCompletion, WeekAssignment

admin.site.register(Roommate)
admin.site.register(Area)
admin.site.register(Task)
admin.site.register(RotationSlot)
admin.site.register(WeekAssignment)
admin.site.register(TaskCompletion)
