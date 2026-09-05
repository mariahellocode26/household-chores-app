import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from chores.models import TaskCompletion, WeekAssignment
from chores.services import ensure_week, week_progress


def _rows_for(assignments):
    """Build the (roommate, area, completions) rows shared by the dashboard
    and the history detail page, ordered by each roommate's fixed position.
    """
    assignments = sorted(assignments, key=lambda wa: wa.roommate.order)
    return [
        {
            "roommate": wa.roommate,
            "area": wa.area,
            "completions": list(wa.task_completions.select_related("task").order_by("task__order", "task__id")),
        }
        for wa in assignments
    ]


def dashboard(request):
    """The shared dashboard: current week's assignments and task checklists.

    Ensures the current week exists (lazily generating it on first visit
    of a new week, plan §12) before rendering it.
    """
    assignments = ensure_week()
    rows = _rows_for(assignments)

    week_start = assignments[0].week_start if assignments else None
    completed_tasks, total_tasks = week_progress(week_start) if week_start else (0, 0)

    return render(
        request,
        "chores/dashboard.html",
        {
            "week_start": week_start,
            "rows": rows,
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
        },
    )


@require_POST
def toggle_task(request, completion_id):
    """Flip one task's completed status; any roommate may do this (plan §5)."""
    completion = get_object_or_404(TaskCompletion, id=completion_id)
    completion.completed = not completion.completed
    completion.save(update_fields=["completed"])

    completed_tasks, total_tasks = week_progress(completion.week_assignment.week_start)

    return render(
        request,
        "chores/_toggle_response.html",
        {
            "completion": completion,
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
        },
    )


def history_list(request):
    """All recorded weeks (including the current one), most recent first.

    Plan §7: history is purely for reviewing past assignments and
    completion, reached via a separate page from the dashboard.
    """
    week_starts = (
        WeekAssignment.objects.order_by("-week_start").values_list("week_start", flat=True).distinct()
    )
    return render(request, "chores/history_list.html", {"week_starts": week_starts})


def history_detail(request, week_start):
    """One past week's assignments and completion status, read-only.

    Deliberately excludes timestamps, who completed each task, and any
    fairness score/statistic (plan §7).
    """
    try:
        week_start = datetime.date.fromisoformat(week_start)
    except ValueError:
        raise Http404("Not a valid week")

    assignments = WeekAssignment.objects.filter(week_start=week_start).select_related("roommate", "area")
    if not assignments:
        raise Http404("No such week")

    rows = _rows_for(assignments)

    return render(request, "chores/history_detail.html", {"week_start": week_start, "rows": rows})
