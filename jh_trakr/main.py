from job_app import (new_app, applied_to_app, rejected_from_app, show_apps)
import sys

usage_msg = (
    "\nusage: jh-trakr [new | applied | rejected |"
    " show [working | applied | rejected]]\n\n"
    "usage: jh-trakr [n | a | r | s [w | a | r]]\n\n"
    "\tjh-trakr n[ew]\n\n\t\tProvides a prompt to enter in information about a"
    " new job application,\n\t\tthis command must be ran first to generate"
    " data which the other commands rely upon\n\n"
    "\tjh-trakr a[pplied]\n\n\t\tAllows you to select which new application"
    " you have applied for to update its status\n\n"
    "\tjh-trakr r[ejected]\n\n\t\tAllows you to select which application that"
    " you applied to has rejected you to update\n\t\tits status\n\n"
    "\tjh-trakr s[how] [w[orking] | a[pplied] | r[ejected]]\n\n\t\tShows all"
    " job application data unless filtered by status\n\n"

)
wrong_show_syntax_msg = (
    "\nshow usage: jh-trakr s[how] [w[orking] | a[pplied] | r[ejected]]\n\n"
    "\tjh-trakr show\n\n\t\tShows all applications and their data\n\n"
    "\tjh-trakr show working\n\n\t\tShows all applications in the working"
    " status\n\n"
    "\tjh-trakr show applied\n\n\t\tShows all applications in the applied"
    " status\n\n"
    "\tjh-trakr show rejected\n\n\t\tShows all applications in the rejected"
    " status\n\n"
)


def main():
    if len(sys.argv) == 2:

        # The startswith calls allows each command to be abbrieviated

        if "new".startswith(sys.argv[1]):
            new_app()

        elif "applied".startswith(sys.argv[1]):
            applied_to_app()

        elif "rejected".startswith(sys.argv[1]):
            rejected_from_app()

        elif "show".startswith(sys.argv[1]):
            show_apps()

        else:
            print(usage_msg)
            sys.exit(1)

    elif len(sys.argv) == 3:

        if not "show".startswith(sys.argv[1]):
            print(usage_msg)
            sys.exit(1)

        if "working".startswith(sys.argv[2]):
            opt = "working"

        elif "applied".startswith(sys.argv[2]):
            opt = "applied"

        elif "rejected".startswith(sys.argv[2]):
            opt = "rejected"

        else:
            print(wrong_show_syntax_msg)
            sys.exit(1)

        show_apps(opt)

    else:
        print(usage_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
