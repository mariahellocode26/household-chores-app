"""Pure functions for the weekly rotation: no DB writes, easy to unit test.

See chores/services.py for the DB-facing "ensure this week exists" logic
that builds on top of these.
"""

import datetime


def week_start_for(date):
    """Return the Monday (as a date) that starts `date`'s week."""
    return date - datetime.timedelta(days=date.weekday())


def week_index_for(week_start):
    """A number that increases by exactly 1 from one Monday to the next.

    Consecutive Mondays are always 7 days apart, so dividing the date's
    ordinal by 7 gives a stable, ever-increasing index with no need to
    store an arbitrary "week 1" epoch anywhere.
    """
    return week_start.toordinal() // 7


def compute_assignments(week_start, roommates, rotation_slots):
    """Return [(roommate, area), ...] for `week_start`.

    `roommates` must be ordered by `order` (ascending) and `rotation_slots`
    by `position` (ascending); both are expected to be the same length N.
    Roommate at position i gets the area whose rotation slot is at
    (i + week_index) % N, cycling through the fixed base rotation shown
    in plan.md's rotation table.
    """
    roommates = list(roommates)
    rotation_slots = list(rotation_slots)
    n = len(rotation_slots)
    week_index = week_index_for(week_start)

    return [
        (roommate, rotation_slots[(roommate.order + week_index) % n].area)
        for roommate in roommates
    ]
