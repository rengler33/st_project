from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import TypeAlias


class City(Enum):
    HIGH = "high"
    LOW = "low"


class DayKind(Enum):
    TRAVEL = "travel"
    FULL = "full"


ReimbursementMatrix: TypeAlias = dict[tuple[DayKind, City], int]


@dataclass(frozen=True)
class ProjectDay:
    day: date
    city: City


@dataclass(frozen=True)
class Project:
    start_date: date
    end_date: date
    city: City

    @property
    def days(self) -> list[ProjectDay]:
        """List of all unique ProjectDays between start_date and end_date, inclusive
        and sorted by date.
        """
        dates = set()
        length_of_span = self.end_date - self.start_date
        for day_count in range(length_of_span.days + 1):
            dates.add(self.start_date + timedelta(days=day_count))
        return [ProjectDay(day=day, city=self.city) for day in sorted(list(dates))]

    def __post_init__(self):
        assert self.start_date <= self.end_date, "start_date must be on or before end_date"


@dataclass
class ProjectGroup:
    projects: list[Project] = field(default_factory=list)

    @property
    def all_days(self) -> list[ProjectDay]:
        """List of all ProjectDays across all projects, sorted by date."""
        all_days = []
        for project in self.projects:
            all_days += project.days
        return sorted(all_days, key=lambda x: x.day)

    def add_project(self, project: Project):
        if not isinstance(project, Project):
            raise ValueError("Must provide a Project")
        self.projects.append(project)


def create_project_group(projects: list[Project]) -> ProjectGroup:
    group = ProjectGroup()
    for project in projects:
        group.add_project(project)
    return group


@dataclass(frozen=True)
class CalculatedProjectDay:
    project_day: ProjectDay
    day_kind: DayKind
    reimbursement_amount: int
