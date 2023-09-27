from datetime import datetime
from pyfzf.pyfzf import FzfPrompt
import sqlite3
import shutil
import os
import re


def sanitize_filename(filename):
    # Pattern to catch illegal filename characters
    pattern = r'[\\/:"*?<>|\s]+'

    # Use re.sub() to replace all matched characters with underscores
    sanitized_filename = re.sub(pattern, '_', filename)

    return sanitized_filename


def new_app():
    """ Obtains job information from user """
    company_input = input("Company: ")
    position_input = input("Position: ")
    location_input = input("Location: ")
    url_input = input("URL: ")

    # Creates db if needed and stores new job app
    with sqlite3.connect("job_apps.db") as con:

        cur = con.cursor()

        create_table_cmd = """
            CREATE TABLE IF NOT EXISTS job_apps (
                id INTEGER PRIMARY KEY,
                company TEXT,
                position TEXT,
                application_status TEXT,
                location TEXT,
                resume_path TEXT,
                url TEXT,
                date TEXT
            );
        """

        cur.execute(create_table_cmd)
        con.commit()

        insert_new_app_cmd = (
            "INSERT INTO job_apps\n"
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

    full_app_path = os.path.join("working", new_app_folder)

    os.makedirs(full_app_path, exist_ok=True)

    resume_template_path = "template/resume.tex"

    dest_app_resume = os.path.join(full_app_path, sanitize_filename(
                                   f"{position_input}-at-{company_input}.tex"))

    shutil.copyfile(resume_template_path, dest_app_resume)


def applied_to_app():
    """ Moves application project files to applied folder and sets status of
    app in database """

    applied_app = FzfPrompt().prompt(os.listdir("working"))[0]

    applied_id = applied_app.split('-')[-1]

    with sqlite3.connect("job_apps.db") as con:

        cur = con.cursor()

        today = datetime.now().strftime("%B %d, %Y")

        resume_path = os.path.join("applied",
                                   applied_app,
                                   f"{applied_app}.tex")

        update_cmd = (
            "UPDATE job_apps\n"
            "SET application_status = 'applied',\n"
            f"\tdate = '{today}',\n"
            f"\tresume_path = '{resume_path}'\n"
            f"WHERE id = {applied_id};"
        )

        cur.execute(update_cmd)
        con.commit()

    os.makedirs("applied", exist_ok=True)

    shutil.move(os.path.join("working", applied_app),
                os.path.join("applied", applied_app))


def rejected_from_app():

    rejected_app = FzfPrompt().prompt(os.listdir("applied"))[0]

    rejected_id = rejected_app.split('-')[-1]

    with sqlite3.connect("job_apps.db") as con:

        cur = con.cursor()

        resume_path = os.path.join("applied/rejected",
                                   rejected_app,
                                   f"{rejected_app}.tex")

        update_cmd = (
            "UPDATE job_apps\n"
            "SET application_status = 'rejected',\n"
            f"\tresume_path = '{resume_path}'\n"
            f"WHERE id = {rejected_id};"
        )

        cur.execute(update_cmd)
        con.commit()

    os.makedirs("applied/rejected", exist_ok=True)

    shutil.move(os.path.join("applied", rejected_app),
                os.path.join("applied/rejected", rejected_app))


def show_apps():
    """
    Have a command which displays the apps without having to worry about sql
    edit main.py to also allow for 3 args so you can run 'make show <status>'
    where <status> is job status
    """
    pass
