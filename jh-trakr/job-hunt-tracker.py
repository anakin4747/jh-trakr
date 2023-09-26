from job_application import JobApp, new_app, applied_to_app, rejected_from_app
import sys

if len(sys.argv) != 2:
    print("Choose an option: new, applied, rejected")
    sys.exit(1)

# Argument options
if sys.argv[1] == "new":
    job_details = new_app()
    job_app = JobApp(*job_details)
    job_app.print_job()

elif sys.argv[1] == "applied":
    applied_to_app()
elif sys.argv[1] == "rejected":
    rejected_from_app()
else:
    print("Choose an option: new, applied, rejected")
    sys.exit(1)


"""
So a job hunt tracker will allow a user to create a new job application
and store the data within a sqlite database


some things to think about

Actions
- New application
- application status change
- create database for jobs
- create time tracking database
- start and stop tracking time for specific job application
- view total time spent this week


Come up with better names

db_stuff:
    db_time_stuff:
        db_time_start(application)
        db_time_stop()
        - the time db will have to querry the job db for a valid application
    db_app_stuff:
        db_create()
        db_change_status()



"""

"""
have a section for input and test user input with pytest

"""
