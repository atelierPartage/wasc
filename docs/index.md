# Web Accessibility Simple Checker

Wasc is a simple tool to check if a list of websites respect some accessibility criteria.

## Installation
To install Wasc, run the following command from the command line:

```bash
pip install wasc
```

## Running an analysis

Getting started is super from example files in directory `data`.
You may try `wasc data/example_websites.csv` as follows:

```bash
$ wasc data/example_websites.csv
Use default criteria
Analysis of 2 websites...
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  3.98it/s]
Results:
{
    "Design Gouv": {
        "Accessibilité": {
            "Lien accessibilité": "https://design.numerique.gouv.fr/misc/accessibilite",
            "Mention accessibilité": "totalement conforme"
        },
        "Mentions légales": {
            "Mentions légales": "https://design.numerique.gouv.fr/misc/mentions-legales"
        }
    },
    "Example": {
        "Accessibilité": {
            "Lien accessibilité": "échec",
            "Mention accessibilité": "échec"
        },
        "Mentions légales": {
            "Mentions légales": "échec"
        }
    }
}
Completed
```

As you can see:

* default criteria are "Accessibilité" and "Mentions légales"
* default output format is `json`.

## Change format

You can choose to print results in csv using `-f csv` option:

```bash
$ wasc data/example_websites.csv -f csv
Use default criteria
Analysis of 2 websites...
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  3.63it/s]
Results:
Organisation;Mention accessibilité;Lien accessibilité;Mentions légales
Design Gouv;totalement conforme;https://design.numerique.gouv.fr/misc/accessibilite;https://design.numerique.gouv.fr/misc/mentions-legales
Example;échec;échec;échec

Completed
```

## Change output

You may specify the output file using `-o out.json` option:

```bash
$ wasc data/example_websites.csv -o out.json
Use default criteria
Analysis of 2 websites...
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  2.75it/s]
Save results in out.json
Completed
```

## Change criteria

Wasc criteria are defined in a YAML formatted file.
An example is given in `data/criteria.yml`.

In the YAML file, a criterion may contain many checkers as follows:
```yaml
Accessibilité :
  - AccessChecker
  - AccessLinkChecker
  - AccessRateChecker
```

The criterion name is "Accessibilité" and it is composed of 3 checkers.

The list of checkers is given in page [Checkers]()