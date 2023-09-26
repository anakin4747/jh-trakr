import sqlite3


# class JobApp:
#
#     def __init__(self, company, position, location, url):
#         self.company = company
#         self.position = position
#         self.location = location
#         self.url = url
#         self.status = "working"
#
#     def set_status(self, status):
#         pass
#
#     def print_job(self):
#         print(f'Company: {self.company}',
#               f'Position: {self.position}',
#               f'Location: {self.location}',
#               f'URL: {self.url}',
#               f'Status: {self.status}')
#

def new_app():
    """ Obtains job information from user """
    company_input = input("Company: ")
    position_input = input("Position: ")
    location_input = input("Location: ")
    url_input = input("URL: ")

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
        con.commit()


def applied_to_app():
    print("applied")


def rejected_from_app():
    print("rejected")
