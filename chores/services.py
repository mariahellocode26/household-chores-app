"""DB-facing logic that builds on the pure functions in chores/rotation.py."""

from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from chores.models import Roommate, RotationSlot, Task, TaskCompletion, WeekAssignment
from chores.rotation import compute_assignments, week_start_for


def ensure_week(week_start=None):
    """Make sure `week_start`'s WeekAssignments (and TaskCompletions) exist.

    Defaults to the current week. Safe to call on every request: if the
    week's assignments already exist, this does nothing and returns them
    unchanged. Guarantees a week is never generated twice (plan §12) by
    checking existence up front and relying on WeekAssignment's DB-level
    uniqueness constraints as a backstop under concurrent requests.
    """
    if week_start is None:
        week_start = week_start_for(timezone.localdate())

    existing = list(
        WeekAssignment.objects.filter(week_start=week_start).select_related("roommate", "area")
    )
    if existing:
        return existing

    roommates = list(Roommate.objects.order_by("order"))
    rotation_slots = list(RotationSlot.objects.select_related("area").order_by("position"))
    assignments = compute_assignments(week_start, roommates, rotation_slots)

    with transaction.atomic():
        created = []
        for roommate, area in assignments:
            week_assignment = WeekAssignment.objects.create(
                week_start=week_start, roommate=roommate, area=area
            )
            tasks = Task.objects.filter(area=area)
            TaskCompletion.objects.bulk_create(
                TaskCompletion(week_assignment=week_assignment, task=task) for task in tasks
            )
            created.append(week_assignment)

    return created


def week_progress(week_start):
    """Return (completed_count, total_count) of tasks for `week_start`."""
    counts = TaskCompletion.objects.filter(week_assignment__week_start=week_start).aggregate(
        total=Count("id"), completed=Count("id", filter=Q(completed=True))
    )
    return counts["completed"] or 0, counts["total"] or 0
