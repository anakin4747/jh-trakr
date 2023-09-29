from job_app import new_app, applied_to_app, rejected_from_app, show_apps
import sys

usage_msg = "\nChoose an option: new, applied, rejected, show\n"
wrong_show_syntax_msg = (
    "\nshow must either be called with no arguments or with any of the "
    "following: \n\tworking, applied, or rejected\n"
)


def main():
    if len(sys.argv) == 2:

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

        if sys.argv[1] == "show":

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

    else:
        print(usage_msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
