# Job Hunt Tracker - Command Line Tool

## Why Command Line Tool

I prefer command line tools for managing tasks and personal projects. So I
created a command line tools which helps me keep track of job applications from
the command line. 

If I have a task I regularly find myself doing I always try to find a way to
migrate it into the command line.

The benefits of command line workflows:

    - Easier to integrate with automation tasks thanks to bash and python
      scripts
    - Easier to manage and integrate with my everyday command line tools vim,
      tmux, and git
    - Fast, compared to previous database applications like Notion
    - Cool

## This Tool

This Python command line app allows me to keep track of job applications in
folders with extra data stored in a SQLite database.

## Testing

This project was prototyped in Bash and tested using the pytest Python library.

The unit tests are in the [tests](tests) directory. They are broken up into
specific files for each function tested.

The tests are run automatically during build as they are specified to run
during the build target of the Makefile.

## Install

## Basic Usage
