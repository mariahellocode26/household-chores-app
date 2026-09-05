# Shared Household Chores Tool — MVP Scope

## 1. Project Goal

A simple tool for roommates sharing an apartment to manage weekly household chores fairly and track task completion.

The core model is:

**Apartment → Areas → Tasks → Weekly Assignment → Completion Tracking**

---

## 2. Target Users

- Roommates sharing an apartment
- MVP assumes a predefined household
- No user authentication

---

## 3. Household Structure

The MVP household consists of:

- 3 roommates: A, B, C
- 3 areas:
  - Kitchen
  - Bathroom
  - Common Area

Each area contains multiple specific chore tasks.

### Example Tasks

#### Kitchen

- Clean counters
- Wash sink
- Mop floor

#### Bathroom

- Clean toilet
- Clean sink
- Mop floor

#### Common Area

- Vacuum
- Dust surfaces
- Organize shared items

---

## 4. Weekly Rotation

Every roommate is assigned exactly one area each week.

The rotation is fully automatic and follows a fixed order.

Example:

| Week | A | B | C |
|---|---|---|---|
| 1 | Kitchen | Bathroom | Common Area |
| 2 | Bathroom | Common Area | Kitchen |
| 3 | Common Area | Kitchen | Bathroom |

A new week's assignments are automatically generated every Monday.

Tasks are due by the end of the week (Sunday).

There are no individual task deadlines.

---

## 5. Task Completion

Each assigned area contains individual tasks.

Roommates mark **individual tasks** as completed.

Rules:

- Tasks can be checked or unchecked.
- Any roommate can check or uncheck a task during the current week.
- Only completed/incomplete status is tracked.
- The system does not record who completed a task.
- Every task counts equally.
- Incomplete tasks remain recorded as incomplete for that specific week.
- Incomplete tasks do not automatically carry over to the next week.

---

## 6. Dashboard

The app opens directly to the shared dashboard.

Everyone sees the same fully transparent dashboard.

The main view is a weekly table:

| Roommate | Assigned Area | Tasks |
|---|---|---|
| A | Kitchen | ☐ Counters ☐ Sink ☐ Floor |
| B | Bathroom | ☐ Toilet ☐ Sink ☐ Floor |
| C | Common Area | ☐ Vacuum ☐ Dust |

The current dashboard shows:

- Current week's assignments
- Individual task checkboxes
- Overall progress, e.g. `7 / 12 tasks completed`

The dashboard does not show previous or future weeks.

---

## 7. History

The system keeps the complete history of past weeks.

History is accessed through a separate **History** page.

Each historical week shows:

- Roommate assignments
- Individual tasks
- Completion/incomplete status

History does not include:

- Completion timestamps
- Who completed a task
- Fairness scores/statistics

There is no fairness summary or scoring in the MVP.

History is purely for reviewing past assignments and completion.

---

## 8. Household Setup

The MVP uses a **predefined household**.

There is no household creation/setup UI.

The household configuration includes:

- Roommates
- Areas
- Tasks
- Rotation order

The configuration is immutable in the MVP.

Roommates cannot be added or removed after setup.

Assignments cannot be manually changed.

---

## 9. Authentication & Access

No real authentication is required.

The app is a shared household dashboard.

No roommate name selection is required when opening the app.

---

## 10. Notifications

No reminders or notifications are included in the MVP.

---

## 11. Data Storage

Use **PostgreSQL** for persistent storage.

The database should preserve:

- Household configuration
- Roommates
- Areas
- Tasks
- Weekly assignments
- Weekly task completion status
- Historical weeks

---

## 12. Weekly Generation

Every Monday, the system automatically creates the new week's assignments according to the fixed rotation.

The system must ensure that the same week is not generated more than once.

---

## 13. Explicitly Out of Scope

The following features are intentionally excluded from the MVP:

- User accounts/authentication
- Household creation UI
- Adding/removing roommates
- Editing household configuration after setup
- Manual assignment changes
- Reminders/notifications
- Task carry-over
- Individual task deadlines
- Task difficulty/weights
- Fairness statistics or scoring
- Completion timestamps
- Tracking who completed a task
- Task comments/notes
- Future-week navigation
- Per-roommate progress indicators

---

## 14. Core MVP User Flow

1. User opens the app.
2. The current week's assignments are displayed.
3. Each roommate has one assigned area.
4. Each area displays its individual chore checklist.
5. Roommates check/uncheck tasks as they complete them.
6. Overall completion progress updates.
7. At the start of Monday, the next week's assignments are automatically generated.
8. The previous week's assignments and completion statuses remain available in History.

---

## 15. MVP Definition of Done

The MVP is successful if three roommates can:

1. Share one predefined apartment configuration.
2. Automatically receive fairly rotating weekly area assignments.
3. See all current assignments in one shared dashboard.
4. Check off individual chores.
5. See overall weekly completion progress.
6. Review previous weeks and their completion statuses.
7. Have all data persist reliably in PostgreSQL.

---

## 16. Scope Summary

### Core Features

- Fixed household
- Fixed roommates
- Fixed areas and tasks
- Automatic weekly rotation
- Individual task checklists
- Shared transparent dashboard
- Overall weekly progress
- Historical weeks
- PostgreSQL persistence
- Automatic Monday assignment generation

### Not in MVP

- Authentication
- Notifications
- Household management
- Manual rotation changes
- Fairness analytics
- Comments
- Advanced deadlines
- Gamification
- Mobile app
- User profiles
- Admin interface