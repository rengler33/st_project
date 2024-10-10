<p align="center">
<img width="617" alt="image" src="https://github.com/user-attachments/assets/adbf243b-3989-4b8b-8f85-1c578810fdf0">
</p>

# 🧵 st_project
The only expense tracking application you'll ever need.
Certain to get Finance's seal of approval!

## Setup

Make sure you have python 3.10+ installed.

1. Clone the repository and `cd` into `st_project`
2. Create a virtual environment `python -m venv .venv`
3. Activate the virtual environment `source .venv/bin/activate`
4. Install the local project `pip install -e .`

## Running the application

If you'd like to input a project by hand, simply run `python -m application`.
Alternatively, you can pipe a file into the script `cat group.csv | python -m application`.

### Input format

The format of input should be in CSV format.

Each record should represent a project.

The order of data for a project should be start date, end date, and city classification ("high" or "low").

Dates should use YYYY-MM-DD format.

Multiple projects should be separated by a newline.

Example input:
```
2015-9-1,2015-9-1,low
2015-9-2,2015-9-6,high
2015-9-6,2015-9-11,low
```
