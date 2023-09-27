from job_app import new_app, applied_to_app, rejected_from_app, show_apps
import sys

usage_msg = "\nChoose an option: new, applied, rejected, show\n"
wrong_show_syntax_msg = (
    "\nshow must either be called with no arguments or with any of the "
    "following: \n\tall, working, applied, or rejected\n"
)

if len(sys.argv) == 2:

    if sys.argv[1] == "new":
        new_app()

    elif sys.argv[1] == "applied":
        applied_to_app()

    elif sys.argv[1] == "rejected":
        rejected_from_app()

    elif sys.argv[1] == "show":
        show_apps()

    else:
        print(usage_msg)
        sys.exit(1)

elif len(sys.argv) == 3:

    if sys.argv[1] == "show":

        if sys.argv[2] not in ["all", "working", "applied", "rejected"]:
            print(wrong_show_syntax_msg)
            sys.exit(1)

        show_apps(sys.argv[2])

    else:
        print(usage_msg)
        sys.exit(1)

else:
    print(usage_msg)
    sys.exit(1)
