# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
import json
import sys

import click
import pandas as pd
from tqdm import tqdm
from pprint import pprint

from wasc.__about__ import __version__
from wasc.checker_factory import checker_factory
from wasc.report import Report
from wasc.utils import read_checkers, read_websites, report_to_csv

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
DEFAULT_CHECKERS = ["AccessChecker", "AccessLinkChecker", "DoctypeChecker", "LangChecker", "LegalChecker"]

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("websites", type=click.Path(exists=True))
@click.option("-c", "--checkers", type=click.Path(exists=True),
              help="Checkers list to use")
@click.option("-o", "--output", default=sys.stdout,
              type=click.File("w"),
              help="Output file [default=stdout]")
@click.option("-f", "--output_format", default = "json",
              type=click.Choice(["json", "csv"], case_sensitive=False),
              help="Output format [default=json]")
@click.version_option(version=__version__, prog_name="wasc")
def wasc(websites, checkers, output, output_format):
    """
    wasc, for Websites Accessibility Criteria Checker,
    helps to evaluate accessibility criteria on a list of websites

    WEBSITES is a CSV file containing a list of websites as couples
    (label,URL)
    """
    checker_names = DEFAULT_CHECKERS
    if checkers:
        click.echo(f"Read checkers from {checkers}")
        checker_names = read_checkers(checkers)
    else :
        click.echo("Use default checkers")
    checkers_list = [checker_factory.create(checker_name) for checker_name in checker_names]
    column_names = ["Organisation", "URL", "Erreur"]
    column_names += [checker.description for checker in checkers_list]
    websites = read_websites(websites)
    click.echo(f"Analysis of {len(websites)} websites...")
    reports = []
    for i in tqdm(range(len(websites))):
        label, url = websites[i]
        reports.append(Report(label, url, checkers_list).execute())
    df = pd.DataFrame(reports, columns=column_names)
    df.set_index(["Organisation"], inplace=True)
    if output == sys.stdout:
        click.echo("Results:")
    else :
        click.echo("Save results in " + output.name)
    if output_format == "json":
        json_load = json.loads(df.to_json(force_ascii=False, orient="index"))
        click.echo(json.dumps(json_load, sort_keys=True, indent=4, ensure_ascii=False), file=output)
    elif output_format == "csv":
        click.echo(df.to_csv(sep=";"), file=output)
    click.echo("Completed")
