"""Seed the fixed MVP household (plan.md §3, §4).

This runs automatically as part of `manage.py migrate`, since the plan
requires a predefined household with no setup UI. It is idempotent
(get_or_create) so re-running migrate never creates duplicates.
"""

from django.db import migrations

ROOMMATES = ["A", "B", "C"]

# area name -> ordered list of task names
AREAS = {
    "Kitchen": ["Clean counters", "Wash sink", "Mop floor"],
    "Bathroom": ["Clean toilet", "Clean sink", "Mop floor"],
    "Common Area": ["Vacuum", "Dust surfaces", "Organize shared items"],
}

# Fixed base rotation order (week 1), per plan.md §4.
ROTATION_ORDER = ["Kitchen", "Bathroom", "Common Area"]


def seed_household(apps, schema_editor):
    Roommate = apps.get_model("chores", "Roommate")
    Area = apps.get_model("chores", "Area")
    Task = apps.get_model("chores", "Task")
    RotationSlot = apps.get_model("chores", "RotationSlot")

    for order, name in enumerate(ROOMMATES):
        Roommate.objects.get_or_create(name=name, defaults={"order": order})

    areas_by_name = {}
    for area_name, task_names in AREAS.items():
        area, _ = Area.objects.get_or_create(name=area_name)
        areas_by_name[area_name] = area
        for task_order, task_name in enumerate(task_names):
            Task.objects.get_or_create(
                area=area, name=task_name, defaults={"order": task_order}
            )

    for position, area_name in enumerate(ROTATION_ORDER):
        RotationSlot.objects.get_or_create(
            area=areas_by_name[area_name], defaults={"position": position}
        )


def unseed_household(apps, schema_editor):
    Roommate = apps.get_model("chores", "Roommate")
    Area = apps.get_model("chores", "Area")

    Roommate.objects.filter(name__in=ROOMMATES).delete()
    Area.objects.filter(name__in=AREAS.keys()).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("chores", "0003_weekassignment_taskcompletion_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_household, unseed_household),
    ]
