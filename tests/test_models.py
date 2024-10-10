from datetime import date

import pytest

from st_project.models import Project, City, ProjectDay, ProjectGroup


def test_cant_create_project_with_end_date_before_start_date():
    with pytest.raises(AssertionError):
        Project(start_date=date(2020, 1, 1), end_date=date(1998, 10, 28), city=City.HIGH)


def test_can_create_project_with_same_start_date_and_end_date():
    Project(start_date=date(2020, 1, 1), end_date=date(2020, 1, 1), city=City.HIGH)


def test_project_days_of_length_one_returns_only_one_project_day():
    project = Project(start_date=date(2020, 3, 15), end_date=date(2020, 3, 15), city=City.LOW)
    assert project.days == [ProjectDay(day=date(2020, 3, 15), city=City.LOW)]


def test_project_days_of_length_two_is_inclusive():
    project = Project(start_date=date(2020, 3, 15), end_date=date(2020, 3, 16), city=City.LOW)
    assert project.days == [
        ProjectDay(day=date(2020, 3, 15), city=City.LOW),
        ProjectDay(day=date(2020, 3, 16), city=City.LOW),
    ]


def test_project_days_of_length_three_is_inclusive():
    project = Project(start_date=date(2020, 3, 15), end_date=date(2020, 3, 17), city=City.LOW)
    assert project.days == [
        ProjectDay(day=date(2020, 3, 15), city=City.LOW),
        ProjectDay(day=date(2020, 3, 16), city=City.LOW),
        ProjectDay(day=date(2020, 3, 17), city=City.LOW),
    ]


def test_project_group_all_days_returns_sorted_list():
    group = ProjectGroup(
        projects=[
            Project(start_date=date(2020, 3, 15), end_date=date(2020, 3, 16), city=City.LOW),
            Project(start_date=date(2020, 1, 2), end_date=date(2020, 1, 3), city=City.HIGH),
            Project(start_date=date(2020, 1, 1), end_date=date(2020, 1, 2), city=City.LOW),
        ]
    )
    assert group.all_days == [
        ProjectDay(day=date(2020, 1, 1), city=City.LOW),
        ProjectDay(day=date(2020, 1, 2), city=City.HIGH),
        ProjectDay(day=date(2020, 1, 2), city=City.LOW),
        ProjectDay(day=date(2020, 1, 3), city=City.HIGH),
        ProjectDay(day=date(2020, 3, 15), city=City.LOW),
        ProjectDay(day=date(2020, 3, 16), city=City.LOW),
    ]


def test_add_projects():
    group = ProjectGroup()
    group.add_project(
        Project(start_date=date(2020, 3, 15), end_date=date(2020, 3, 16), city=City.LOW)
    )
    group.add_project(
        Project(start_date=date(2020, 3, 15), end_date=date(2020, 3, 16), city=City.LOW)
    )
    group.add_project(
        Project(start_date=date(2020, 3, 16), end_date=date(2020, 3, 17), city=City.LOW)
    )
    assert len(group.projects) == 3
