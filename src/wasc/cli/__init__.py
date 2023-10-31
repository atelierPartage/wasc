# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
import datetime
import json
import sys

import bs4
import click
import pandas as pd
from tqdm import tqdm
from trafilatura.downloads import add_to_compressed_dict, buffered_downloads, load_download_buffer

from wasc.__about__ import __version__
from wasc.checker_factory import checker_factory
from wasc.utils import FAIL, OK, read_checkers, read_websites

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
DEFAULT_CHECKERS = [
    "AccessChecker", "AccessLinkChecker", "AccessRateChecker",
    "DoctypeChecker", "LangChecker", "LegalChecker",
    "ContactLinkChecker"
]

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("websites", type=click.Path(exists=True))
@click.option("-c", "--checkers", type=click.Path(exists=True),
              help="Checkers list to use")
@click.option("-f", "--output_format", default = "json",
              type=click.Choice(["json", "csv"], case_sensitive=False),
              help="Output format [default=json]")
@click.option("-l", "--list_checkers", is_flag=True, default=False,
              help="List known checkers [default=False]")
@click.option("-o", "--output", default=sys.stdout,
              type=click.File("w"),
              help="Output file [default=stdout]")
@click.version_option(version=__version__, prog_name="wasc")
def wasc(websites, checkers, output_format, list_checkers, output):
    """
    Websites Accessibility Criteria Checker,
    helps to evaluate accessibility criteria on a list of websites

    WEBSITES is a CSV file containing a list of websites as couples
    "label";"URL"
    """
    # If list_checkers then list checkers and stops
    if list_checkers:
        for checker in checker_factory.available():
            click.echo(checker)
        return
    # Reads and creates checker list
    checker_names = DEFAULT_CHECKERS
    if checkers:
        click.echo(f"Read checkers from {checkers}")
        checker_names = read_checkers(checkers)
    else :
        click.echo("Use default checkers")
    checkers_list = [checker_factory.create(checker_name) for checker_name in checker_names]

    # Sets column names for DataFrame using checkers descriptions
    column_names = ["Organisation", "URL", "Erreur"] + [checker.description for checker in checkers_list]

    # Reads the list of web sites
    websites = read_websites(websites)
    websites_dict = dict(zip([ws[1].strip("/") for ws in websites], [ws[0] for ws in websites]))
    url_list = [ws[1] for ws in websites]

    # Launch analysis
    click.echo(f"Analysis of {len(websites)} websites...")
    threads = 8
    dl_dict = add_to_compressed_dict(url_list)
    mybuffer, dl_dict = load_download_buffer(dl_dict)
    results = []
    with tqdm(total=len(url_list)) as pbar:
        for url, response in buffered_downloads(mybuffer, threads, decode=False):
            label = websites_dict[url.strip("/")]
            bs_obj = None
            error = ""
            if response:
                if response.status == OK :
                    bs_obj = bs4.BeautifulSoup(response.data, "html.parser")
                else:
                    error = "HTML Error Status " + str(response.status)
            else:
                error = "Problème lors du téléchargement"
            starter = [label, url, error]
            analysis = [checker.execute(bs_obj, url) if bs_obj else FAIL for checker in checkers_list]
            results.append(starter + analysis)
            pbar.update(1)

    # Creates the DataFrame from results
    df = pd.DataFrame(results, columns=column_names)
    df.set_index(["Organisation"], inplace=True)

    # Output results given -o output and -f output_format
    if output == sys.stdout:
        click.echo("Results:")
    else :
        click.echo("Save results in " + output.name)
    if output_format == "json":
        json_load = json.loads(df.to_json(force_ascii=False, orient="index"))
        click.echo(json.dumps(json_load, sort_keys=True, indent=4, ensure_ascii=False), file=output)
    elif output_format == "csv":
        today = datetime.datetime.today()
        output.write("# " + today.strftime("%d/%m/%y %H:%M:%S") + "\n")
        click.echo(df.to_csv(sep=";"), file=output)
    click.echo("Completed")
