"""An example application with CSV input demonstrating the API of st_project."""

from datetime import datetime, date
import csv
import sys

from .st_project.models import Project, City, create_project_group
from .st_project.services import calculate_project_group_reimbursement, DayKind

REIMBURSEMENT_MATRIX = {
    (DayKind.TRAVEL, City.LOW): 45,
    (DayKind.TRAVEL, City.HIGH): 55,
    (DayKind.FULL, City.LOW): 75,
    (DayKind.FULL, City.HIGH): 85,
}


def process_csv_projects(input) -> list[Project]:
    csv_reader = csv.reader(input)
    projects = []
    for start_date, end_date, city in csv_reader:
        projects.append(_create_project(start_date, end_date, city))
    return projects


def _create_project(start_date, end_date, city) -> Project:
    return Project(
        start_date=_parse_date(start_date.strip()),
        end_date=_parse_date(end_date.strip()),
        city=City(city.strip()),
    )


def _parse_date(date_: str) -> date:
    dt = datetime.strptime(date_, "%Y-%m-%d")
    return dt.date()


def main(projects: list[Project], matrix):
    """Calculate the reimbursement total for a group of projects."""
    group = create_project_group(projects)
    total_reimbursement = calculate_project_group_reimbursement(group, matrix)
    print(total_reimbursement)


if __name__ == "__main__":
    if not sys.stdin.isatty():  # process a piped csv
        text_input = sys.stdin
    else:  # ask for input
        print("Provide project data separated by a newline per project.")
        print("Project data is in the form of start date, end date, low/high.")
        print("(enter a final empty newline to start processing)")
        print("*" * 25)
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        text_input = lines

    try:
        projects = process_csv_projects(text_input)
    except ValueError as e:
        print(e)
        exit(1)

    if not projects:
        print("No projects supplied")
        exit(1)

    main(projects, REIMBURSEMENT_MATRIX)
