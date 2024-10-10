<p align="center">
<img width="617" alt="image" src="https://github.com/user-attachments/assets/adbf243b-3989-4b8b-8f85-1c578810fdf0">
</p>

# 🧵 st_project
The only expense tracking application you'll ever need.
Certain to get Finance's seal of approval!

## Setup

1. Make sure you have python 3.10+ installed, `python --version`
2. Clone the repository and `cd` into the directory
3. There are no project dependencies so a virtual environment is not required

### Running the application

You can pipe a file into the script `cat group_1.csv | python -m application`.

Four test cases are provided in the repository:

- `cat group_1.csv | python -m application`
- `cat group_2.csv | python -m application`
- `cat group_3.csv | python -m application`
- `cat group_4.csv | python -m application`

Alternatively, if you'd like to input a project by hand, simply run `python -m application`.

#### Input format

The format of input should be in CSV format.

Each record should represent a project.

The order of data for a project should be start date, end date, and city classification ("high" or "low").

Dates should use YYYY-MM-DD format.

Multiple projects should be separated by a newline.

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

To run test: `pytest tests`.
