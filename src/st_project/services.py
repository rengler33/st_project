from enum import Enum
from st_project.models import ProjectGroup, City, ProjectDay


class DayKind(Enum):
    TRAVEL = "travel"
    FULL = "full"


def calculate_project_group_reimbursement(
    group: ProjectGroup, matrix: dict[tuple[DayKind, City], int]
) -> int:
    """Calculate the total reimbursement of a ProjectGroup"""
    # reduce to only unique days,
    #   preferring HIGH cost city if overlapping  TODO confirm?
    unique_days = _merge_all_days_of_project_group(group)
    # chunk all dates into contiguous date ranges
    chunked_days = _chunk_consecutive_days(unique_days)
    # assign first and last day as TRAVEL days
    # assign any days in between as FULL days
    travel_days, full_days = _categorize_chunked_days(chunked_days)
    # sum all values for TRAVEL and FULL days based on their HIGH or LOW city
    travel_days_cost = _calculate_days_cost(travel_days, matrix, DayKind.TRAVEL)
    full_days_cost = _calculate_days_cost(full_days, matrix, DayKind.FULL)
    return travel_days_cost + full_days_cost


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


def _categorize_chunked_days(
    chunked_days: list[list[ProjectDay]],
) -> tuple[list[ProjectDay], list[ProjectDay]]:
    """Categorize a set of chunked ProjectDays into TRAVEL or FULL days."""
    travel_days = set()
    full_days = set()
    for chunk in chunked_days:
        match chunk:
            case [travel_1]:
                travel_days.add(travel_1)
            case [travel_1, travel_2]:
                travel_days.add(travel_1)
                travel_days.add(travel_2)
            case [travel_1, *full, travel_2]:
                travel_days.add(travel_1)
                travel_days.add(travel_2)
                for day in full:
                    full_days.add(day)
    return (
        sorted(list(travel_days), key=lambda x: x.day),
        sorted(list(full_days), key=lambda x: x.day),
    )


def _calculate_days_cost(
    days: list[ProjectDay], matrix: dict[tuple[DayKind, City], int], day_kind: DayKind
) -> int:
    total = 0
    for day in days:
        total += matrix[(day_kind, day.city)]
    return total
