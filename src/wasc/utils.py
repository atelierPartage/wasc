# SPDX-FileCopyrightText: 2023-present Guillaume Collet <bilouweb@free.fr>
#
# SPDX-License-Identifier: CECILL-2.1
"""
This module provides some reading functions
"""
import pandas as pd

HEADER = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    "referer" : "https://www.google.com/"
    }

def read_checkers(filename) :
    """
    Reads the list of checkers.

    Parameters
    ----------
    filename : str
        File name containing list of checkers

    Returns
    -------
    : list
        A list of checker names
    """
    with open(filename, encoding = "utf-8") as config_file :
        return [line.strip() for line in config_file]

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

def report_to_csv(reports, checkers_list):
    res = []
    return res
