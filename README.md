<p align="center">
<img width="617" alt="image" src="https://github.com/user-attachments/assets/adbf243b-3989-4b8b-8f85-1c578810fdf0">
</p>

# 🧵 st_project
The only expense tracking application you'll ever need.
Certain to get Finance's seal of approval!

## What is this?

Business logic for calculating reimbursements is built into the st_project library (located in `src/st_project`).
A command-line interface for using the library has been built as a demo application in `application.py`.

## Setup

1. Make sure you have python 3.10+ installed, `python --version`
2. Clone the repository and `cd` into the directory
3. There are no project dependencies so a virtual environment is not required

### Running the demo application

You can pipe a CSV file into the script `cat group_1.csv | python -m application`.

Four test cases are provided in the repository:

- `cat group_1.csv | python -m application`
- `cat group_2.csv | python -m application`
- `cat group_3.csv | python -m application`
- `cat group_4.csv | python -m application`

Alternatively, if you'd like to input a project by hand, simply run `python -m application` and follow the prompt.

#### Input format

The format of input should be in CSV format.

Each record should represent a Project.

A Project consists of a start date, end date, and city-cost classification ("high" or "low").

Dates should use YYYY-MM-DD format.

Multiple Projects can be provided as a Project group, and should be separated by a newline.

Example input:
```csv
2015-9-1,2015-9-1,low
2015-9-2,2015-9-6,high
2015-9-6,2015-9-11,low
```


## Dev Setup

To install project development dependencies, use `uv sync`. This will create a virtual environment
in the `.venv` folder if it doesn't exist.

(to install `uv` see [uv docs](https://docs.astral.sh/uv/getting-started/installation/))

Activate your virtual environment `source .venv/bin/activate`.

### Running tests

To run tests, from the top directory run: `pytest tests`.
