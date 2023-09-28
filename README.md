# Job Hunt Tracker - Command Line Tool

I prefer command line tools for managing tasks and personal projects. So I
created this command line tool which helps me keep track of job applications from
the command line. 

If I have a task I regularly find myself doing I always try to find a way to
migrate it into the command line.

The benefits of command line workflows:

    - Easier to integrate with automation tasks thanks to bash and python scripts
    - Easier to manage and integrate with my everyday command line tools vim, tmux, and git
    - Fast, compared to previous database applications like Notion
    - Cool

This Python command line app allows me to keep track of job applications in
folders with extra data stored in a SQLite database.

## Pytest Testing

This project was prototyped in
[Bash](https://github.com/anakin4747/job-hunt-workflow/) and tested using the
pytest Python library.

The unit tests are in the [tests](tests) directory. They are broken up into
specific files for each function tested.

The tests are run automatically during build as they are specified to run
during the build target of the Makefile.


## Basic Usage

The application has 4 main commands:

    jh_trakr new
    jh_trakr applied
    jh_trakr rejected
    jh_trakr show

The **new** command allows you to input information about the new job application
to which you are applying:

    $ jh_trakr new

    Company: Cool Company
    Position: Cool Position
    Location: Ottawa      
    URL: https://cool.company.com/cool-job-posting

After the **new** command has been successfully completed a directory called
*working* is created in your current working directory. Inside *working* should
be a folder for the newly created job application.

    $ ls working

    Cool_Position-at-Cool_Company-1

Since I write my resumes in LaTeX the application copies a template of a LaTeX
document that resembles the barebones of my resume into the directory inside
*working* and this now becomes my project folder for that application.

You can also query the database that was created from using the **new** command
with the command **show**.

    $ jh_trakr show

    +----+--------------+---------------+--------------------+----------+---
    | id |   company    |   position    | application_status | location | ...
    +----+--------------+---------------+--------------------+----------+---
    | 1  | Cool Company | Cool Position |      working       | Ottawa   | ...
    +----+--------------+---------------+--------------------+----------+---

This will display the extra data that is stored about the job applications as
well as their statuses.

The next command available is the **applied**. This command is for when you
(me) are done updating your specific resume and actually apply for the job.

Since this application was initially prototyped in Bash, I used the awesome
command line fuzzy finder fzf to select which working job application you
applied for.

    $ jh_trakr applied

This command will take you to a prompt to select from the applications in the
*working* directory. After you hit enter that project folder in the *working*
directory is moved to the *applied* directory and data is updated in the
database to reflect the date which you applied and the changed status.

    $ jh_trakr show

    +----+--------------+---------------+--------------------+----------+---
    | id |   company    |   position    | application_status | location | ...
    +----+--------------+---------------+--------------------+----------+---
    | 1  | Cool Company | Cool Position |      applied       | Ottawa   | ...
    +----+--------------+---------------+--------------------+----------+---

The last command is **rejected** and its use should be pretty obvious. It is
the same as **applied** except it moves the specific application folder to the
*applied/rejected* directory.
