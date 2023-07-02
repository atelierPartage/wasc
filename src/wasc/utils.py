# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
This module provides some reading functions
"""
import pandas as pd
import yaml


def read_criteria_config(filename) :
    """
    Reads the list of criteria.
    Each criterion is associated with a list of checkers
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
     : list
        A list of of (websites, url)
    """
    df = pd.read_csv(filename, sep=";", comment="#", header = None, names=["org", "url"], skipinitialspace=True)
    return list(zip(df.org, df.url))

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

def find_link(access_tag, root_url):
    while access_tag and access_tag.name != "a" and access_tag.name != "html":
        access_tag = access_tag.parent
    try :
        return check_and_correct_url(access_tag.attrs["href"], root_url)
    except KeyError :
        pass

def dict_to_csv(indict):
    res = {"Organisation" : []}
    for org, subdict in indict.items():
        res["Organisation"].append(org)
        for checkdict in subdict.values():
            for key, val in checkdict.items():
                if key not in res:
                    res[key] = []
                res[key].append(val)
    return res
