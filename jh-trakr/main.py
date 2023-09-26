
from job_app import new_app, applied_to_app, rejected_from_app
import sys

if len(sys.argv) != 2:
    print("Choose an option: new, applied, rejected")
    sys.exit(1)

# Argument options
if sys.argv[1] == "new":
    new_app()

elif sys.argv[1] == "applied":
    applied_to_app()

elif sys.argv[1] == "rejected":
    rejected_from_app()

else:
    print("Choose an option: new, applied, rejected")
    sys.exit(1)
