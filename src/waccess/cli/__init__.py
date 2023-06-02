# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
import sys

import click

from waccess.__about__ import __version__
from waccess.utils import read_criteria_config, read_websites

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
DEFAULT_CRIT_DICT = { "Balise head" : ["FLBT01", "FLBT02"]}

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("websites", type=click.File("r"))
@click.option("-c", "--criteria", type=click.Path(exists=True),
              help="Criteria configuration file (yaml)")
@click.option("-o", "--output", default=sys.stdout,
              type=click.File("w"),
              help="Output file [default=stdout]")
@click.option("-f", "--output_format", default = "json",
              type=click.Choice(["json", "csv"], case_sensitive=False),
              help="Output format [default=json]")
@click.version_option(version=__version__, prog_name="waccess")
def waccess(websites, criteria, output, output_format):
    """
    waccess, for Websites Accessibility Criteria Checker,
    helps to evaluate accessibility criteria on a list of websites

    WEBSITES is a CSV file containing a list of websites as couples
    (label,URL)
    """
    crit_dict = DEFAULT_CRIT_DICT
    if criteria:
        crit_dict = read_criteria_config(criteria)
    click.echo(crit_dict, file=output)
    click.echo(read_websites(websites), file=output)
