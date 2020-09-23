#!/usr/bin/env python
"""Module to check the environment variables

This script uses Python to access the system's os.envion and
generates a report file (by default going to "/tmp/report.txt")
with a formatted string output.
"""
from argparse import ArgumentParser
import os
import sys

def gen_environment_report(filename, str_format="%50s:%50s\n"):
    """Generate Environment Report

    1) Accesses os.environ for environmental variables

    Parameters
    ----------
    filename : str
        Output report file location

    str_format : str
        Given "%40s:%50s\n",
            The key field will be space-padded to 40 characters
            The value field will be space-padded 50 characters.
    """
    # --------------  if file exist, ask user if overwrite  -----------------
    if os.path.isfile(filename):
        if sys.version_info.major > 2:
            # Python3, use input
            ans = input("%s exists, overwrite? (Y/N)"%filename)
        else:
            # Python2, use raw_input
            ans = raw_input("%s exists, overwrite? (Y/N)"%filename)
        if not ans.lower() in ["y", "yes"]:
            print("Aborting.")
            return

    # -------------------  generate report  ---------------------------------
    with open(filename, "w") as f:
        print("Generating file...")
        f.write("# Auto-generated Environment" + "\n"*2)

        # ENVIRONMENT Variables
        for key in os.environ.keys():
            if "PATH" in key:
                # for path, separate by ":" for better readability
                my_path = os.environ[key]
                toks = my_path.split(":")
                my_key = key
                for tok in toks:
                    f.write(str_format%(my_key, tok))
                    my_key = ""
            else:
                # default, write key and value
                f.write(str_format%(key, os.environ[key]))

        # TODO: what other information will be useful?
        print("Report completed (%s)"%filename)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--report", default="/tmp/report.txt",
        help="Report file to generate")
    parser.add_argument("--format", default="%50s:%50s\n",
        help="Configure format of printout")
    args = parser.parse_args()

    # call report generator
    gen_environment_report(args.report, str_format=args.format)
