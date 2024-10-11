from .models import (
    CalculatedProjectDay,
    City,
    DayKind,
    ProjectDay,
    ProjectGroup,
    ReimbursementMatrix,
)


def generate_calculated_project_days(
    group: ProjectGroup, matrix: ReimbursementMatrix
) -> list[CalculatedProjectDay]:
    """
    Given a ProjectGroup, return a list of CalculatedProjectDays which represent the classification
    of the day and provide that day's associated cost based on the provided cost matrix.

    Explanation:
        - reduce all dates across Projects in the ProjectGroup to unique days (preferring HIGH cost
            city if there is a conflict).
        - chunk all of the dates into contiguous date ranges
        - with each contiguous chunk, assign first and last day as TRAVEL days, and any days in
            between as FULL days
        - assign the cost of each day based on their TRAVEL / FULL and HIGH / LOW classifications,
            using a provided cost matrix
    """
    unique_days = _merge_all_days_of_project_group(group)
    chunked_days = _chunk_consecutive_days(unique_days)
    travel_days, full_days = _categorize_chunked_days(chunked_days)
    calculated_travel_days = [
        _create_calculated_project_day(day, DayKind.TRAVEL, matrix) for day in travel_days
    ]
    calculated_full_days = [
        _create_calculated_project_day(day, DayKind.FULL, matrix) for day in full_days
    ]
    return sorted(calculated_travel_days + calculated_full_days, key=lambda x: x.project_day.day)


def calculate_project_group_reimbursement(group: ProjectGroup, matrix: ReimbursementMatrix) -> int:
    """Calculate the total reimbursement amount of a ProjectGroup given a cost matrix."""
    calculated_project_days = generate_calculated_project_days(group, matrix)
    reimbursements = [day.reimbursement_amount for day in calculated_project_days]
    return sum(reimbursements)


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
    sorted_dates = sorted(days, key=lambda x: x.day)  # ensure sorted for algorithm

    chunks = []
    current_chunk = [sorted_dates[0]]

    for i, current_day in enumerate(sorted_dates[1:], start=1):
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


def _create_calculated_project_day(day: ProjectDay, day_kind: DayKind, matrix: ReimbursementMatrix):
    reimbursement_amount = matrix[(day_kind, day.city)]
    return CalculatedProjectDay(
        project_day=day, day_kind=day_kind, reimbursement_amount=reimbursement_amount
    )
