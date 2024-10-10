"""This module tests the example project sets provided"""
from datetime import date

from st_project.models import City, Project, create_project_group
from st_project.services import DayKind
from st_project.services import calculate_project_group_reimbursement

TEST_REIMBURSEMENT_MATRIX = {
    (DayKind.TRAVEL, City.LOW): 45,
    (DayKind.TRAVEL, City.HIGH): 55,
    (DayKind.FULL, City.LOW): 75,
    (DayKind.FULL, City.HIGH): 85,
}


def test_group_1():
    """
    Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15
    """
    # 9/1/15 TRAVEL/LOW = 45
    # 9/2/15 FULL/LOW = 75
    # 9/3/15 TRAVEL/LOW = 45
    # total: 165
    projects = [
        Project(start_date=date(2015, 9, 1), end_date=date(2015, 9, 3), city=City.LOW),
    ]
    group = create_project_group(projects)
    assert calculate_project_group_reimbursement(group, TEST_REIMBURSEMENT_MATRIX) == 165


def test_group_2():
    """
    Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15
    Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15
    Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15
    """
    # 9/1/15 TRAVEL/LOW = 45
    # 9/2/15 FULL/HIGH = 85
    # 9/3/15 FULL/HIGH = 85
    # 9/4/15 FULL/HIGH = 85
    # 9/5/15 FULL/HIGH = 85
    # 9/6/15 FULL/HIGH = 85
    # 9/7/15 FULL/LOW = 75
    # 9/8/15 TRAVEL/LOW = 45
    # total: 590
    projects = [
        Project(start_date=date(2015, 9, 1), end_date=date(2015, 9, 1), city=City.LOW),
        Project(start_date=date(2015, 9, 2), end_date=date(2015, 9, 6), city=City.HIGH),
        Project(start_date=date(2015, 9, 6), end_date=date(2015, 9, 8), city=City.LOW),
    ]
    group = create_project_group(projects)
    assert calculate_project_group_reimbursement(group, TEST_REIMBURSEMENT_MATRIX) == 590


def test_group_3():
    """
    Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15
    Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15
    Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15
    """
    # 9/1/15 TRAVEL/LOW = 45
    # 9/2/15 FULL/LOW = 75
    # 9/3/15 TRAVEL/LOW = 45

    # 9/5/15 TRAVEL/HIGH = 55
    # 9/6/15 FULL/HIGH = 85
    # 9/7/15 FULL/HIGH = 85
    # 9/8/15 TRAVEL/HIGH = 55
    # total: 445
    projects = [
        Project(start_date=date(2015, 9, 1), end_date=date(2015, 9, 3), city=City.LOW),
        Project(start_date=date(2015, 9, 5), end_date=date(2015, 9, 7), city=City.HIGH),
        Project(start_date=date(2015, 9, 8), end_date=date(2015, 9, 8), city=City.HIGH),
    ]
    group = create_project_group(projects)
    assert calculate_project_group_reimbursement(group, TEST_REIMBURSEMENT_MATRIX) == 445


def test_group_4():
    """
    Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15
    Project 2: Low Cost City Start Date: 9/1/15 End Date: 9/1/15
    Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15
    Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15
    """
    # 9/1/15 TRAVEL/LOW = 45
    # 9/2/15 FULL/HIGH = 85
    # 9/3/15 TRAVEL/HIGH = 55
    # total: 185
    projects = [
        Project(start_date=date(2015, 9, 1), end_date=date(2015, 9, 1), city=City.LOW),
        Project(start_date=date(2015, 9, 1), end_date=date(2015, 9, 1), city=City.LOW),
        Project(start_date=date(2015, 9, 2), end_date=date(2015, 9, 2), city=City.HIGH),
        Project(start_date=date(2015, 9, 2), end_date=date(2015, 9, 3), city=City.HIGH),
    ]
    group = create_project_group(projects)
    assert calculate_project_group_reimbursement(group, TEST_REIMBURSEMENT_MATRIX) == 185
