from datetime import date
from dataclasses import dataclass, field
from enum import Enum
from typing import Self


class City(Enum):
    HIGH = "high"
    LOW = "low"


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
        """List of all ProjectDays between start_date and end_date, inclusive."""
        ...


@dataclass
class ProjectGroup:
    projects: set[Project] = field(default_factory=set)

    @property
    def all_days(self) -> list[ProjectDay]:
        """List of all ProjectDays across all projects."""
        ...

    def add_project(self, project: Project) -> Self:
        if not isinstance(project, Project):
            raise ValueError("Must provide a Project")
        self.projects.add(project)
        return self


def create_project_group(projects: list[Project]):
    group = ProjectGroup()
    for project in projects:
        group.add_project(project)
    return group
