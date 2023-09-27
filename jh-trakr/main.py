from job_app import new_app, applied_to_app, rejected_from_app, show_apps
import sys

usage_msg = "Choose an option: new, applied, rejected, show"

if len(sys.argv) == 2:

    if sys.argv[1] == "new":
        new_app()

    elif sys.argv[1] == "applied":
        applied_to_app()

    elif sys.argv[1] == "rejected":
        rejected_from_app()

    else:
        print(usage_msg)
        sys.exit(1)

elif len(sys.argv) == 3:
    if sys.argv[1] == "show":
        show_apps(sys.argv[2])
    else:
        print(usage_msg)
        sys.exit(1)
else:
    print(usage_msg)
    sys.exit(1)
