from django.db import models


class Roommate(models.Model):
    """A member of the fixed household. Immutable after seeding (plan §8)."""

    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(
        unique=True,
        help_text="Fixed position in the rotation cycle (0-based).",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Area(models.Model):
    """A cleanable area of the household (e.g. Kitchen). Immutable after seeding."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RotationSlot(models.Model):
    """The fixed base rotation: which area sits at each position in the cycle.

    Combined with each Roommate's `order`, this determines every week's
    assignments (see chores/rotation.py) without needing to store every
    future week up front. Immutable after seeding.
    """

    position = models.PositiveSmallIntegerField(unique=True)
    area = models.OneToOneField(Area, on_delete=models.CASCADE, related_name="rotation_slot")

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"Position {self.position}: {self.area.name}"


class Task(models.Model):
    """A single chore within an area (e.g. "Wash sink"). Immutable after seeding."""

    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(
        default=0,
        help_text="Display order within the area's checklist.",
    )

    class Meta:
        ordering = ["area", "order", "id"]

    def __str__(self):
        return f"{self.area.name}: {self.name}"


class WeekAssignment(models.Model):
    """One roommate's area assignment for one week.

    `week_start` is the Monday identifying the week (see
    chores/rotation.py:week_start_for). Together with `roommate`, it is
    unique so the same week's assignments can never be generated twice
    (plan §12).
    """

    week_start = models.DateField()
    roommate = models.ForeignKey(Roommate, on_delete=models.CASCADE, related_name="week_assignments")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="week_assignments")

    class Meta:
        ordering = ["-week_start", "roommate__order"]
        constraints = [
            models.UniqueConstraint(fields=["week_start", "roommate"], name="unique_roommate_per_week"),
            models.UniqueConstraint(fields=["week_start", "area"], name="unique_area_per_week"),
        ]

    def __str__(self):
        return f"{self.week_start}: {self.roommate.name} -> {self.area.name}"


class TaskCompletion(models.Model):
    """Whether one task was completed, scoped to a specific week's assignment.

    Deliberately minimal per plan §5/§7: just a completed/incomplete flag.
    No timestamp and no record of who completed it.
    """

    week_assignment = models.ForeignKey(
        WeekAssignment, on_delete=models.CASCADE, related_name="task_completions"
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completions")
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["task__order", "task__id"]
        constraints = [
            models.UniqueConstraint(fields=["week_assignment", "task"], name="unique_task_per_week_assignment"),
        ]

    def __str__(self):
        status = "done" if self.completed else "not done"
        return f"{self.week_assignment}: {self.task.name} ({status})"
