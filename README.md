# 100 Portfolio Project Ideas With Datasets: companion files

Free companion files for the book **100 Portfolio Project Ideas With Datasets: Real Public Data, a Sharp Question and a Step-by-Step Approach for Every Project** by Mathew Kariuki.

The book gives 100 data analysis portfolio projects, each built on a public dataset, with a question to answer and a suggested approach. This repository holds the full project list as a spreadsheet you can sort and filter, the practice data and code from the book's worked example (Riverton Bike Share, a fictional city scheme), and templates for planning, writing up and checking your projects.

## Download

Click the green **Code** button above, then **Download ZIP**. Unzip it somewhere sensible, such as your Documents folder.

## What's here

| Path | What it is |
| --- | --- |
| `projects/portfolio_projects.xlsx` | All 100 projects with theme, level, time, tools, dataset, publisher, link, access and question (filterable) |
| `projects/portfolio_projects.csv` | The same list as a CSV file |
| `data/riverton_trips_2026_09.csv` | Practice bike share trips for Chapter 4 (45,512 trips, September 2026) |
| `data/riverton_stations.csv` | The 35 Riverton stations |
| `book_code/ch04_bike_share.py` | Every code example from Chapter 4, in order |
| `templates/project_README_template` | A blank project README in the layout from Chapter 5 (.md and .docx) |
| `templates/project_planner` | A one-page planner for choosing and scoping a project (.md and .docx) |
| `templates/portfolio_checklist` | The publishing checklist and a whole-portfolio review (.md and .docx) |
| `scripts/make_data.py` | The script that generated the practice data |
| `scripts/check_links.py` | Checks which dataset links in the project list still respond |

## Quick start

1. Install Python, then run:

   ```
   pip install -r requirements.txt
   ```

2. Open this folder in VS Code (**File > Open Folder**) or a terminal.
3. Run the Chapter 4 worked example:

   ```
   python book_code/ch04_bike_share.py
   ```

   It prints each step's output and saves the chart to `output/ch04_weekday_profile.png`.

4. To check the dataset links (takes a couple of minutes):

   ```
   python scripts/check_links.py
   ```

Paths assume this folder is your working directory. Tested with Python 3.13 and pandas 3.0.

## Dataset links

Every link was checked in October 2026. Public data moves, so if a link fails, search for the dataset name and publisher, and check this repository for updates. Spotted a broken or moved link? Please open an issue.

## Get the book

Paperback and Kindle editions are on Amazon. The PDF bundle with a printable cheat sheet is on Gumroad at [mathewkariuki.gumroad.com](https://mathewkariuki.gumroad.com).

## About

Riverton Bike Share and every person and business in the book's examples are fictional. The public datasets listed belong to their publishers and carry their own licences. The practice data, code and templates in this repository are free to use for learning. The book itself is © 2026 Mathew Kariuki.
