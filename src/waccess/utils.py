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
        try :
            config_data = yaml.safe_load(config_file)
        except yaml.YAMLError as exc :
            msg = f"Unable to read {filename}, check the file format"
            raise RuntimeError(msg) from exc
        return config_data

def read_websites(file) :
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
    return [(line[0].strip(), line[1].strip()) for line in csv.reader(file)]
