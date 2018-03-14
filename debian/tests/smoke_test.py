# -*- coding: utf-8 -*-
#
# debian/tests/smoke_test.py
#
# Copyright © 2016–2017 Ben Finney <bignose@debian.org>
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied.

""" Post-install Python smoke test for use in Debian autopkgtest.

    Written for both Python 2 and Python 3, to test all installed
    versions of a package.

    Smoke test the distribution::
        --distribution=DISTRIBUTION

    Smoke test one or more modules::
        --module=MODULE_FOO --module=MODULE_BAR --module=MODULE_BAZ
    """

import sys
import argparse
import importlib
import pkg_resources


def emit_implementation():
    """ Emit the details of the current Python implementation.

        :return: ``None``.
        """
    sys.stdout.write(
            "Interpreter: {command}\n{version}\n".format(
                command=sys.executable, version=sys.version))


def emit_distribution(name):
    """ Get the distribution `name` and emit its representation.

        :param name: Name of the distribution to retrieve.
        :return: ``None``.
        """
    distribution = pkg_resources.get_distribution(name)
    sys.stdout.write(
            "Distribution ‘{name}’:\n\t{distribution!r}\n".format(
                name=name, distribution=distribution))


def emit_module(name):
    """ Import the module `name` and emit the module representation.

        :param name: Full name of the module to import.
        :return: ``None``.
        """
    module = importlib.import_module(name)
    sys.stdout.write(
            "Package ‘{name}’:\n\t{module!r}\n".format(
                name=name, module=module))


def suite(args):
    """ Run the full suite of tests.

        :param args: Namespace of arguments parsed from `ArgumentParser`.
        :return: ``None``.
        """
    emit_implementation()

    if args.distribution_name:
        emit_distribution(args.distribution_name)

    for module_name in args.module_names:
        emit_module(module_name)


class SmokeTestArgumentParser(argparse.ArgumentParser):
    """ Command-line argument parser for this program. """

    def __init__(self, *args, **kwargs):
        super(SmokeTestArgumentParser, self).__init__(*args, **kwargs)

        self.add_argument(
                '--distribution',
                dest='distribution_name', type=str,
                metavar="DISTRIBUTION", help=(
                    "Test the Python distribution named DISTRIBUTION."))
        self.add_argument(
                '--module',
                dest='module_names', type=str, nargs='+',
                metavar="MODULE", help=(
                    "Test the Python module named MODULE."))


def main(argv=None):
    """ Mainline code for this module.

        :param argv: Sequence of all command line arguments.
            (Default: `sys.argv`)
        :return: The exit status (integer) for exit from the process.
        """
    exit_status = 0

    if argv is None:
        argv = sys.argv

    try:
        program_name = argv[0]
        parser = SmokeTestArgumentParser(prog=program_name)
        args = parser.parse_args(argv[1:])

        suite(args)

    except SystemExit as exc:
        exit_status = exc.code

    return exit_status


if __name__ == "__main__":
    exit_status = main(sys.argv)
    sys.exit(exit_status)


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
