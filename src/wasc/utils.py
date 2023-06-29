# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
This module provides some reading functions
"""
import csv

import yaml


def read_criteria_config(filename) :
    """
    Reads the list of criteria. Each criterion is associated qith a list of checkers

    The file must be in YAML format.

    Parameters
    ----------
    filename : str
        File name containing list of criteria

    Returns
    -------
    config_data : dict
        A dictionary of criteria associated with the list of checkers
    """
    with open(filename, encoding = "utf-8") as config_file :
        return yaml.safe_load(config_file)

def read_websites(filename) :
    """
    Reads the websites list, each website is a couple (label, URL)

    Parameters
    ----------
    filename : File
        File containing websites list in CSV format

    Returns
    -------
     : dict
        A dictionary of websites (keys are labels and values URLs)
    """
    with open(filename, encoding = "utf-8") as url_file :
        return [(line[0].strip(), line[1].strip()) for line in csv.reader(url_file)]

def check_and_correct_url(target_url : str, root_url : str) -> str :
    """
    This method check if the target_url is truncated and, if so,
    recompose from the root_url

    Parameters
    ----------
    target_url : str
        URL of a page in a website, may be truncated
    root_url : str
        The root URL of the current website

    Returns
    -------
    access_url : str
        The URL of the desired web page
    """

    # remove trailing backslash
    target_url = target_url.strip("/")
    root_url = root_url.strip("/")

    # If not truncated
    if target_url.startswith("http") :
        return target_url

    # Else if the root_url end overlap the target_url start
    target_subpath = target_url.split("/")
    root_subpath = root_url.split("/")
    if target_subpath[0] == root_subpath[-1]:
        return root_url + "/" + "/".join(target_subpath[1:])

    # Else concatenate
    return root_url + "/" + target_url
