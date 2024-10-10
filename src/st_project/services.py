from enum import Enum
from st_project.models import ProjectGroup, City, ProjectDay


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
    unique_days = _merge_all_days_of_project_group(group)
    # chunk all dates into contiguous date ranges
    #   assign first and last day as TRAVEL days
    #   assign any days in between as FULL days
    # sum all values for TRAVEL and FULL days based on their HIGH or LOW city
    ...


def _merge_all_days_of_project_group(group: ProjectGroup) -> list[ProjectDay]:
    merged_days = {}
    for day in group.all_days:
        if day.day not in merged_days or day.city == City.HIGH:
            merged_days[day.day] = day
    return list(merged_days.values())
