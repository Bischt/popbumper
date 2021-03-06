#!/usr/bin/env python
# vim: set syntax=python:

import argparse
import sys

from pb.popbumper_command import PopbumperCommand  # noqa: E402


def main():
    """
    Sample function.

    Parameters:
        get_all:
            Get all resources.
        get: string
            Get specific resource.

    """

    args, raw_args = parse_arguments()
    print("RAW ARGS: {}".format(raw_args))
    if args.port == "80":
        host = args.host
    else:
        host = args.host + ":" + args.port

    popbumper_command = PopbumperCommand(host)

    param, param_data = parse_raw_args(raw_args)

    operation = popbumper_command.playfield_operations()[args.resource]
    operation(args.action, param, param_data)

    exit(0)


def parse_raw_args(raw_args):
    param = None
    param_data = None

    for arg in raw_args:
        if param is None:
            param = arg
        elif param_data is None:
            param_data = arg

    return param, param_data


def parse_arguments():
    """
    Figure out argparse's help from docstring thing
    :return:
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=main.__doc__,
        prog='pb'
    )
    parser.add_argument(
        "resource",
        choices=PopbumperCommand.resource_names(),
        help=f"Resource to inspect {PopbumperCommand.resource_names()}",
    )
    parser.add_argument(
        "action",
        choices=PopbumperCommand.action_names(),
        help=f"Action to take {PopbumperCommand.action_names()}",
    )

    parser.add_argument('-H', '--host', default="127.0.0.1", help="API hostname")
    parser.add_argument('-p', '--port', default="8080", help="API port")
    parser.add_argument('-v', '--verbose', action="count", default=0, help="Expand output to include everything")

    args, extra_args = parser.parse_known_args()
    return args, extra_args


if __name__ == "__main__":
    sys.exit(main())
