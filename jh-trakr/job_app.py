import sqlite3
import os
import re


def sanitize_filename(filename):
    # Pattern to catch illegal filename characters
    pattern = r'[\\/:"*?<>|]+'

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
    with sqlite3.connect("job_app.db") as con:

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

    dest_app_resume = os.path.join(full_app_path,
                                   f"{position_input}-at-{company_input}.tex")

    os.system(f"cp {resume_template_path} {dest_app_resume}")


def applied_to_app():
    print("applied")


def rejected_from_app():
    print("rejected")


def show_apps():
    """
    Have a command which displays the apps without having to worry about sql
    edit main.py to also allow for 3 args so you can run 'make show <status>'
    where <status> is job status
    """
    pass
