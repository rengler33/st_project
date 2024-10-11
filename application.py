"""An demo application utilizing CSV input demonstrating the API of st_project library."""

import csv
import sys
from datetime import datetime, date

from src.st_project.models import City, DayKind, Project, create_project_group
from src.st_project.services import calculate_project_group_reimbursement

REIMBURSEMENT_MATRIX = {
    (DayKind.TRAVEL, City.LOW): 45,
    (DayKind.TRAVEL, City.HIGH): 55,
    (DayKind.FULL, City.LOW): 75,
    (DayKind.FULL, City.HIGH): 85,
}


def _request_csv_input():
    print("Provide project data separated by a newline per project.")
    print("Project data is in the form of start date, end date, low/high (cost).")
    print("(enter a final empty newline to start processing)")
    print("*" * 25)
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return lines


def _process_csv_projects(input) -> list[Project]:
    csv_reader = csv.reader(input)
    projects = []
    for start_date, end_date, city in csv_reader:
        projects.append(_create_project(start_date, end_date, city))
    return projects


def _create_project(start_date: str, end_date: str, city: str) -> Project:
    return Project(
        start_date=_parse_date(start_date.strip()),
        end_date=_parse_date(end_date.strip()),
        city=City(city.strip()),
    )


def _parse_date(date_: str) -> date:
    dt = datetime.strptime(date_, "%Y-%m-%d")
    return dt.date()


if __name__ == "__main__":
    if not sys.stdin.isatty():  # process a piped csv
        text_input = sys.stdin
    else:
        text_input = _request_csv_input()

    try:
        projects = _process_csv_projects(text_input)
    except ValueError as e:
        print(f"Error loading input: {e}")
        exit(1)

    if not projects:
        print("No valid Projects supplied")
        exit(1)

    group = create_project_group(projects)
    total_reimbursement = calculate_project_group_reimbursement(group, REIMBURSEMENT_MATRIX)
    print(total_reimbursement)
