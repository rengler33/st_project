from datetime import date
from dataclasses import dataclass
from enum import Enum


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
    projects: set[Project]

    @property
    def all_days(self) -> list[ProjectDay]:
        """List of all ProjectDays across all projects."""
        ...


class DayKind(Enum):
    TRAVEL = "travel"
    FULL = "full"


reimbursement_matrix = {
    (DayKind.TRAVEL, City.LOW): 45,
    (DayKind.TRAVEL, City.HIGH): 55,
    (DayKind.FULL, City.LOW): 75,
    (DayKind.FULL, City.HIGH): 85,
}


def calculate_project_group_reimbursement(
    group: ProjectGroup, matrix: dict[tuple[DayKind, City], int]
) -> int:
    """Calculate the total reimbursement of a ProjectGroup"""
    # reduce to only unique days,
    #   preferring HIGH cost city if overlapping  TODO confirm?
    # chunk all dates into contiguous date ranges
    #   assign first and last day as TRAVEL days
    #   assign any days in between as FULL days
    # sum all values for TRAVEL and FULL days based on their HIGH or LOW city
    ...
