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
    chunk_days = _chunk_consecutive_days(unique_days)
    #   assign first and last day as TRAVEL days
    #   assign any days in between as FULL days
    # sum all values for TRAVEL and FULL days based on their HIGH or LOW city
    ...


def _merge_all_days_of_project_group(group: ProjectGroup) -> list[ProjectDay]:
    """Reduce a ProjectGroup to a list of ProjectDays containing only one ProjectDay per date. If
    the date of the ProjectDay is duplicated but one is in a high-cost city, prefer that
    classification.
    """
    merged_days = {}
    for day in group.all_days:
        if day.day not in merged_days or day.city == City.HIGH:
            merged_days[day.day] = day
    return list(merged_days.values())


def _chunk_consecutive_days(days: list[ProjectDay]) -> list[list[ProjectDay]]:
    """Chunk a list of ProjectDays into lists of continuous days. `days` should contain only
    unique dates."""
    sorted_dates = sorted(days, key=lambda x: x.day)  # ensure sorted

    chunks = []
    current_chunk = [sorted_dates[0]]

    for i, current_day in enumerate(sorted_dates[1:], 1):
        previous_day = sorted_dates[i - 1]
        if (current_day.day - previous_day.day).days == 1:
            current_chunk.append(current_day)
        else:
            chunks.append(current_chunk)
            current_chunk = [current_day]

    chunks.append(current_chunk)

    return chunks
