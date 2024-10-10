from datetime import datetime, date
import csv
import sys

from st_project.models import ProjectGroup, Project, City, create_project_group
from st_project.services import calculate_project_group_reimbursement, DayKind

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
        projects.append(
            Project(
                start_date=parse_date(start_date), end_date=parse_date(end_date), city=City(city)
            )
        )
    return projects


def parse_date(date_: str) -> date:
    try:
        dt = datetime.strptime(date_, "%Y-%m-%d")
        return dt.date()
    except ValueError:
        print("Dates must be in format %Y-%m-%d, e.g. 2020-01-12 or 2020-1-7")
        raise


if __name__ == "__main__":
    if not sys.stdin.isatty():
        projects = process_csv_projects(sys.stdin)
    else:
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        print(lines)
        projects = process_csv_projects(lines)

    group = create_project_group(projects)
    print(calculate_project_group_reimbursement(group, REIMBURSEMENT_MATRIX))
