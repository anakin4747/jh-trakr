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


no_fzf_err_msg = (
    "\nCannot find fzf\n\n"
    "\tThis project relies on your system having fzf\n\n"
    "\tPlease install fzf for this application to function correctly\n\n"
    "Linux:\n\tapt install fzf\n\n"
    "MacOS:\n\tbrew install fzf\n\n"
    "Windows:\n\tchoco install fzf\n\n"
    "GitHub:\n\thttps://github.com/junegunn/fzf\n\n"
)


def sanitize_filename(filename):
    """ Pattern to catch illegal filename characters """
    pattern = r'[\\/:"\'*?<>|\s]+'

    # Use re.sub() to replace all matched characters with underscores
    sanitized_filename = re.sub(pattern, '_', filename)

    return sanitized_filename


def new_app(database=STD_DB, test_args=None, work_dir=WORKING_DIR) -> int:
    """ Obtains job information from user, and creates a application folder in
    the working directory and updates the database to reflect the status """

    if test_args is None:
        company_input = input("Company: ").lstrip().rstrip()
        position_input = input("Position: ").lstrip().rstrip()
        location_input = input("Location: ").lstrip().rstrip()
        url_input = input("URL: ").rstrip()
    else:
        # For testing to get around input() function
        company_input, position_input, location_input, url_input = test_args

    # Removes db suffix from database string
    db_no_suffix = database.split('.')[0]

    # Creates db if needed and stores new job app
    with sqlite3.connect(database) as con:

        cur = con.cursor()

        cur.execute(
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
        con.commit()

        cur.execute(
            f"INSERT INTO {db_no_suffix}\n"
            "(company, position, application_status, location, url)\n"
            "VALUES\n"
            f"('{company_input}', '{position_input}', 'working',"
            f"'{location_input}', '{url_input}');"
        )
        con.commit()

        """ Save autogenerated id of last entry so I can find which db entry it
        is from the name of the application folder """
        last_id = cur.lastrowid

    # Create working folder and new application folder
    title = sanitize_filename(f"{position_input}-at-{company_input}")
    new_app_folder = f"{title}-{last_id}"
    full_app_path = os.path.join(work_dir, new_app_folder)
    os.makedirs(full_app_path, exist_ok=True)

    # Copy resume template to new application folder
    resume_template_path = os.path.join("template", "resume.tex")
    # errors out if missing so fix that
    # Make this file configurable
    dest_app_resume = os.path.join(full_app_path, f"{title}.tex")
    shutil.copyfile(resume_template_path, dest_app_resume)

    return last_id


def applied_to_app(database=STD_DB, test_args=None,
                   work_dir=WORKING_DIR, applied_dir=APPLIED_DIR):
    """ Moves application project files to applied folder and sets status of
    application in database """

    # Check files exist to ensure there is a working application
    if not os.path.exists(work_dir):
        print("\nNo working directory - Try calling 'jh-trakr new' first\n",
              file=sys.stderr)
        sys.exit(1)

    if not os.listdir(work_dir):
        print("\nNo working application - Try calling 'jh-trakr new' first\n",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(database):
        print("\nNo database file - Try calling 'jh-trakr new' first\n",
              file=sys.stderr)
        sys.exit(1)

    if test_args is None:
        # Prompt user to select application folder which they applied for
        try:
            applied_app = FzfPrompt().prompt(os.listdir(work_dir))[0]
        except SystemError:
            print(no_fzf_err_msg, file=sys.stderr)
            sys.exit(1)

    else:
        # Get around fzf prompt in testing
        applied_app = test_args

    # Grab id from folder name so it can be found in db
    applied_id = applied_app.split('-')[-1]

    # Remove .db suffix from database name
    db_no_suffix = database.split('.')[0]

    today = datetime.now().strftime("%B %d, %Y")

    resume_path = os.path.join(applied_dir, applied_app, f"{applied_app}.tex")

    with sqlite3.connect(database) as con:

        cur = con.cursor()

        cur.execute(
            f"UPDATE {db_no_suffix}\n"
            "SET application_status = 'applied',\n"
            f"\tdate = '{today}',\n"
            f"\tresume_path = '{resume_path}'\n"
            f"WHERE id = {applied_id};"
        )
        con.commit()

    # Create applied directory if it doesn't exist
    os.makedirs(applied_dir, exist_ok=True)

    # Move application folder from working directory to applied
    shutil.move(os.path.join(work_dir, applied_app),
                os.path.join(applied_dir, applied_app))


def rejected_from_app(database=STD_DB, test_args=None,
                      applied_dir=APPLIED_DIR, rej_dir=REJ_DIR):
    """ Moves applied apps to rejected """

    # Check files exist to ensure there is an applied application
    if not os.path.exists(applied_dir):
        print("\nNo applied directory - Try calling 'jh-trakr new && jh-trakr"
              " applied' first\n", file=sys.stderr)
        sys.exit(1)

    if not os.listdir(applied_dir):
        print("\nNo applied application - Try calling 'jh-trakr new &&"
              " jh-trakr applied' first\n", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(database):
        print("\nNo database file - Try calling 'jh-trakr new && jh-trakr"
              " applied' first\n", file=sys.stderr)

        sys.exit(1)

    if test_args is None:
        # Prompt user to select application folder which they got rejected from
        try:
            rejected_app = FzfPrompt().prompt(os.listdir(applied_dir))[0]
        except SystemError:
            print(no_fzf_err_msg, file=sys.stderr)
            sys.exit(1)
    else:
        # Get around fzf prompt in testing
        rejected_app = test_args

    # Grab id from folder name so it can be found in db
    rejected_id = rejected_app.split('-')[-1]

    # Remove .db suffix from database name
    db_no_suffix = database.split('.')[0]

    resume_path = os.path.join(rej_dir, rejected_app, f"{rejected_app}.tex")

    with sqlite3.connect(database) as con:

        cur = con.cursor()

        cur.execute(
            f"UPDATE {db_no_suffix}\n"
            "SET application_status = 'rejected',\n"
            f"\tresume_path = '{resume_path}'\n"
            f"WHERE id = {rejected_id};"
        )
        con.commit()

    # Create rejected directory if it doesn't exist
    os.makedirs(rej_dir, exist_ok=True)

    # Move application folder from applied directory to rejected
    shutil.move(os.path.join(applied_dir, rejected_app),
                os.path.join(rej_dir, rejected_app))


def show_apps(opt="all", database=STD_DB):
    """
    Have a command which displays the apps without having to worry about sql
    edit main.py to also allow for 3 args so you can run 'make show <status>'
    where <status> is job status
    """
    if not os.path.exists(database):
        print("\nNo database file - Try calling 'jh-trakr new' first\n",
              file=sys.stderr)
        sys.exit(1)

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
