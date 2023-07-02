# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
import json
import sys

import click
import pandas as pd
from tqdm import tqdm

from wasc.__about__ import __version__
from wasc.criterion import Criterion
from wasc.report import Report
from wasc.utils import dict_to_csv, read_criteria_config, read_websites

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
DEFAULT_CRIT_DICT = { "Accessibilité" : ["AccessChecker", "AccessLinkChecker"], "Mentions légales" : ["MentionsLegalesChecker"]}

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("websites", type=click.Path(exists=True))
@click.option("-c", "--criteria", type=click.Path(exists=True),
              help="Criteria configuration file (yaml)")
@click.option("-o", "--output", default=sys.stdout,
              type=click.File("w"),
              help="Output file [default=stdout]")
@click.option("-f", "--output_format", default = "json",
              type=click.Choice(["json", "csv"], case_sensitive=False),
              help="Output format [default=json]")
@click.version_option(version=__version__, prog_name="wasc")
def wasc(websites, criteria, output, output_format):
    """
    wasc, for Websites Accessibility Criteria Checker,
    helps to evaluate accessibility criteria on a list of websites

    WEBSITES is a CSV file containing a list of websites as couples
    (label,URL)
    """
    crit_dict = DEFAULT_CRIT_DICT
    if criteria:
        click.echo(f"Read criteria from {criteria}")
        crit_dict = read_criteria_config(criteria)
    else :
        click.echo("Use default criteria")
    crit_list = [Criterion(crit, checkers) for crit, checkers in crit_dict.items()]
    websites = read_websites(websites)
    click.echo(f"Analysis of {len(websites)} websites...")
    report = {}
    for i in tqdm(range(len(websites))):
        label, url = websites[i]
        report[label] = Report(label, url, crit_list).execute()
    if output == sys.stdout:
        click.echo("Results:")
    else :
        click.echo("Save results in " + output.name)
    if output_format == "json":
        click.echo(json.dumps(report, sort_keys=True, indent=4, ensure_ascii=False), file=output)
    elif output_format == "csv":
        res = dict_to_csv(report)
        click.echo(pd.DataFrame(res).to_csv(sep=";", index=False), file=output)
    click.echo("Completed")
