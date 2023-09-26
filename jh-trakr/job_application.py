import sqlite3
import os


class JobApp:

    def __init__(self, company, position, location, url):
        self.company = company
        self.position = position
        self.location = location
        self.url = url
        self.status = "working"

    def set_status(self, status):
        pass

    def print_job(self):
        print(f'Company: {self.company}',
              f'Position: {self.position}',
              f'Location: {self.location}',
              f'URL: {self.url}',
              f'Status: {self.status}')


def new_app() -> list:
    """ Obtains job information from user """
    company_input = input("Company: ")
    position_input = input("Position: ")
    location_input = input("Location: ")
    url_input = input("URL: ")

    con = sqlite3.connect("job_app.db")

    cur = con.cursor()

    if os.path.isfile("job_app.db"):
        print("Database exists")
    else:
        print("Creating database")
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

    return [company_input, position_input, location_input, url_input]


def applied_to_app():
    print("applied")


def rejected_from_app():
    print("rejected")
