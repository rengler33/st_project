from datetime import date
from st_project.models import ProjectGroup, City, Project, ProjectDay
from st_project.services import _merge_all_days_of_project_group, _chunk_consecutive_days


def test_merge_all_days_of_project_group():
    # TODO there may be more edge cases that what's captured here, maybe break out?
    group = ProjectGroup(
        projects=[
            # duplicate Project
            Project(start_date=date(2020, 1, 1), end_date=date(2020, 1, 1), city=City.LOW),
            Project(start_date=date(2020, 1, 1), end_date=date(2020, 1, 1), city=City.LOW),
            # overlap with same city
            Project(start_date=date(2020, 1, 1), end_date=date(2020, 1, 3), city=City.LOW),
            # overlap with different city
            Project(start_date=date(2020, 1, 2), end_date=date(2020, 1, 4), city=City.HIGH),
            # gap then more dates
            Project(start_date=date(2020, 1, 10), end_date=date(2020, 1, 11), city=City.LOW),
            # out of order dates
            Project(start_date=date(2020, 1, 9), end_date=date(2020, 1, 10), city=City.HIGH),
        ]
    )
    assert _merge_all_days_of_project_group(group) == [
        ProjectDay(day=date(2020, 1, 1), city=City.LOW),
        ProjectDay(day=date(2020, 1, 2), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 3), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 4), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 9), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 10), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 11), city=City.LOW),
    ]


def test_chunk_consecutive_days():
    days = [
        ProjectDay(day=date(2020, 1, 11), city=City.LOW),
        ProjectDay(day=date(2020, 1, 2), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 1), city=City.LOW),
        ProjectDay(day=date(2020, 1, 4), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 9), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 10), city=City.HIGH),
    ]

    expected = [
        [
            ProjectDay(day=date(2020, 1, 1), city=City.LOW),
            ProjectDay(day=date(2020, 1, 2), city=City.HIGH),
        ],
        [ProjectDay(day=date(2020, 1, 4), city=City.HIGH)],
        [
            ProjectDay(day=date(2020, 1, 9), city=City.HIGH),
            ProjectDay(day=date(2020, 1, 10), city=City.HIGH),
            ProjectDay(day=date(2020, 1, 11), city=City.LOW),
        ],
    ]
    assert _chunk_consecutive_days(days) == expected
