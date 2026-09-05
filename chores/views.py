from django.http import HttpResponse


def home(request):
    """Placeholder home view.

    This will be replaced by the real dashboard (see _docs/tasks.md, task 10).
    For now it only exists to prove the project is wired up end-to-end.
    """
    return HttpResponse("Household Chores")
