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

This project was prototyped in Bash. Checkout the original version [here](https://github.com/anakin4747/job-hunt-workflow/).


## Installation

To install everything in this repo:

    - Clone this repo

    $ git clone https://github.com/anakin4747/jh-trakr.git

    - Change into the directory

    $ cd jh-trakr

    - Run make install

    $ make install

    - Test that it installed

    $ jh-trakr

Since this was initially written in bash it used the incredible command line
fuzzy finder, fzf. So this version also uses it and core features rely on it
being installed on your system.

See [fzf](https://github.com/junegunn/fzf) for installation of fzf.


## Pytest Testing

To run the current unit tests, follow the above installation steps for the full
install to ensure the tests were installed, then run pytest or the make target
test:

    $ pytest

    or

    $ make test

The unit tests are in the [tests/unit](tests/unit) directory. They are broken
up into specific files for each function tested.

Custom pytest fixtures for this project can be found in [tests/conftest.py](tests/conftest.py)

I plan on parameterizing most of the tests to reduce repeated functionality and
to allow for easy integration with the faker module so that I can run the tests
with an arbitrary amount of data.

So far most key functionalities are covered with the tests.

I do plan on also writing functional tests when I can.


## Basic Usage

Run the program without any arguments to see the basic usage menu:

    $ jh-trakr

    usage: jh-trakr [new | applied | rejected | show [working | applied | rejected]]

    usage: jh-trakr [n | a | r | s [w | a | r]]

        jh-trakr n[ew]

                Provides a prompt to enter in information about a new job application,
                this command must be ran first to generate data which the other commands rely upon

        jh-trakr a[pplied]

                Allows you to select which new application you have applied for to update its status

        jh-trakr r[ejected]

                Allows you to select which application that you applied to has rejected you to update
                its status

        jh-trakr s[how] [w[orking] | a[pplied] | r[ejected]]

                Shows all job application data unless filtered by status


The application has 4 main commands:

    $ jh-trakr new
    $ jh-trakr applied
    $ jh-trakr rejected
    $ jh-trakr show

All commands can be abbrieviated to a single letter if desired

The **new** command allows you to input information about the new job application
to which you are applying:

    $ jh-trakr new

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

    $ jh-trakr show

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

    $ jh-trakr applied

This command will take you to a prompt to select from the applications in the
*working* directory. After you hit enter that project folder in the *working*
directory is moved to the *applied* directory and data is updated in the
database to reflect the date which you applied and the changed status.

    $ jh-trakr show

    +----+--------------+---------------+--------------------+----------+---
    | id |   company    |   position    | application_status | location | ...
    +----+--------------+---------------+--------------------+----------+---
    | 1  | Cool Company | Cool Position |      applied       | Ottawa   | ...
    +----+--------------+---------------+--------------------+----------+---

You can also pass **working**, **applied**, or **rejected** to the
**show** command.

    $ jh-trakr show working
        ...
    $ jh-trakr show applied
        ...
    $ jh-trakr show rejected
        ...

The last command is **rejected** and its use should be pretty obvious. It is
the same as **applied** except it moves the specific application folder to the
*applied/rejected* directory.

Note that the commands **applied** and **rejected** rely on the fzf command
line tool. If this is not installed these commands will error out with
instructions for installing fzf.
