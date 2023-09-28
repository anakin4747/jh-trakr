from datetime import datetime
from pyfzf.pyfzf import FzfPrompt
from tabulate import tabulate
import sqlite3
import shutil
import sys
import os
import re

STD_DB = "job_apps.db"
WORKING_DIR = "working"
APPLIED_DIR = "applied"
REJ_DIR = os.path.join(APPLIED_DIR, "rejected")


def sanitize_filename(filename):
    """ Pattern to catch illegal filename characters """
    pattern = r'[\\/:"\'*?<>|\s]+'

    # Use re.sub() to replace all matched characters with underscores
    sanitized_filename = re.sub(pattern, '_', filename)

    return sanitized_filename


def new_app(database=STD_DB, test_args=None, work_dir=WORKING_DIR):
    """ Obtains job information from user """
    if test_args is None:
        company_input = input("Company: ")
        position_input = input("Position: ")
        location_input = input("Location: ")
        url_input = input("URL: ")
    else:
        company_input, position_input, location_input, url_input = test_args

    db_no_suffix = database.split('.')[0]

    # Creates db if needed and stores new job app
    with sqlite3.connect(database) as con:

        cur = con.cursor()

        create_table_cmd = (
            f"CREATE TABLE IF NOT EXISTS {db_no_suffix}(\n"
            "\tid INTEGER PRIMARY KEY,\n"
            "\tcompany TEXT,\n"
            "\tposition TEXT,\n"
            "\tapplication_status TEXT,\n"
            "\tlocation TEXT,\n"
            "\tresume_path TEXT,\n"
            "\turl TEXT,\n"
            "\tdate TEXT\n"
            ");"
        )

        cur.execute(create_table_cmd)
        con.commit()

        insert_new_app_cmd = (
            f"INSERT INTO {db_no_suffix}\n"
            "(company, position, application_status, location, url)\n"
            "VALUES\n"
            f"('{company_input}', '{position_input}', 'working',"
            f"'{location_input}', '{url_input}');"
        )
        cur.execute(insert_new_app_cmd)
        last_id = cur.lastrowid
        con.commit()

    new_app_folder = sanitize_filename(
        f"{position_input}-at-{company_input}-{last_id}")

    full_app_path = os.path.join(work_dir, new_app_folder)

    os.makedirs(full_app_path, exist_ok=True)

    resume_template_path = "template/resume.tex"

    dest_app_resume = os.path.join(full_app_path, sanitize_filename(
                                   f"{position_input}-at-{company_input}.tex"))

    shutil.copyfile(resume_template_path, dest_app_resume)

    return last_id


def applied_to_app(database=STD_DB,
                   test_args=None,
                   work_dir=WORKING_DIR,
                   applied_dir=APPLIED_DIR):
    """ Moves application project files to applied folder and sets status of
    app in database """

    if not os.path.exists(work_dir):
        print("No working directory")
        sys.exit(1)

    if not os.listdir(work_dir):
        print("No working application")
        sys.exit(1)

    if not os.path.exists(database):
        print("No database file")
        sys.exit(1)

    if test_args is None:
        applied_app = FzfPrompt().prompt(os.listdir(work_dir))[0]
    else:
        applied_app = test_args

    applied_id = applied_app.split('-')[-1]

    db_no_suffix = database.split('.')[0]

    with sqlite3.connect(database) as con:

        cur = con.cursor()

        today = datetime.now().strftime("%B %d, %Y")

        resume_path = os.path.join(applied_dir,
                                   applied_app,
                                   f"{applied_app}.tex")

        update_cmd = (
            f"UPDATE {db_no_suffix}\n"
            "SET application_status = 'applied',\n"
            f"\tdate = '{today}',\n"
            f"\tresume_path = '{resume_path}'\n"
            f"WHERE id = {applied_id};"
        )

        cur.execute(update_cmd)
        con.commit()

    os.makedirs(applied_dir, exist_ok=True)

    shutil.move(os.path.join(work_dir, applied_app),
                os.path.join(applied_dir, applied_app))


def rejected_from_app(database=STD_DB,
                      test_args=None,
                      applied_dir=APPLIED_DIR,
                      rej_dir=REJ_DIR):
    """ Moves applied apps to rejected """

    if not os.path.exists(applied_dir):
        print("No applied directory")
        sys.exit(1)

    if not os.listdir(applied_dir):
        print("No applied application")
        sys.exit(1)

    if not os.path.exists(database):
        print("No database file")
        sys.exit(1)

    if test_args is None:
        rejected_app = FzfPrompt().prompt(os.listdir(applied_dir))[0]
    else:
        rejected_app = test_args

    rejected_id = rejected_app.split('-')[-1]

    db_no_suffix = database.split('.')[0]

    with sqlite3.connect(database) as con:

        cur = con.cursor()

        resume_path = os.path.join(rej_dir,
                                   rejected_app,
                                   f"{rejected_app}.tex")

        update_cmd = (
            f"UPDATE {db_no_suffix}\n"
            "SET application_status = 'rejected',\n"
            f"\tresume_path = '{resume_path}'\n"
            f"WHERE id = {rejected_id};"
        )

        cur.execute(update_cmd)
        con.commit()

    os.makedirs(rej_dir, exist_ok=True)

    shutil.move(os.path.join(applied_dir, rejected_app),
                os.path.join(rej_dir, rejected_app))


def show_apps(opt="all", database=STD_DB):
    """
    Have a command which displays the apps without having to worry about sql
    edit main.py to also allow for 3 args so you can run 'make show <status>'
    where <status> is job status
    """

    db_no_suffix = database.split('.')[0]

    with sqlite3.connect(database) as con:

        cur = con.cursor()

        if opt == "all":
            query = f"SELECT * FROM {db_no_suffix};"
        else:
            query = (
                f"SELECT * FROM {db_no_suffix}\n"
                f"WHERE application_status = '{opt}';"
            )

        records = cur.execute(query).fetchall()

        headers = [desc[0] for desc in cur.description]

        table = tabulate(records, headers, tablefmt="pretty")

        print(table)
