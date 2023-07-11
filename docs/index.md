# Web Accessibility Simple Checker

Wasc is a simple tool to check if a list of websites respect some accessibility criteria.

## Installation
To install Wasc, run the following command from the command line:

```bash
pip install wasc
```

## Running an analysis

Getting started is super easy from example files in directory `data`.
You may try `wasc data/example_websites.csv` as follows:

```bash
$ wasc data/example_websites.csv                                                  
Use default checkers
Analysis of 2 websites...
100%|███████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  2.33it/s]
Results:
{
    "Design Gouv": {
        "Doctype": "html",
        "Erreur": "",
        "Lang": "fr",
        "Lien Contact": "https://design.numerique.gouv.fr/contact",
        "Lien accessibilité": "https://design.numerique.gouv.fr/misc/accessibilite",
        "Mention accessibilité": "totalement conforme",
        "Mentions légales": "https://design.numerique.gouv.fr/misc/mentions-legales",
        "Taux d'accessibilité": "100%",
        "URL": "https://design.numerique.gouv.fr/"
    },
    "Example": {
        "Doctype": "html",
        "Erreur": "",
        "Lang": "échec",
        "Lien Contact": "échec",
        "Lien accessibilité": "échec",
        "Mention accessibilité": "échec",
        "Mentions légales": "échec",
        "Taux d'accessibilité": "échec",
        "URL": "http://example.com/"
    }
}
Completed
```

The output always contains `Organisation`, `Erreur` and `URL`.

## Change output format

You can choose to print results in csv using `-f csv` option:

```bash
$ wasc data/example_websites.csv -f csv
Use default checkers
Analysis of 2 websites...
100%|███████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  3.00it/s]
Results:
Organisation;URL;Erreur;Mention accessibilité;Lien accessibilité;Taux d'accessibilité;Doctype;Lang;Mentions légales;Lien Contact
Design Gouv;https://design.numerique.gouv.fr/;;totalement conforme;https://design.numerique.gouv.fr/misc/accessibilite;100%;html;fr;https://design.numerique.gouv.fr/misc/mentions-legales;https://design.numerique.gouv.fr/contact
Example;http://example.com/;;échec;échec;échec;html;échec;échec;échec

Completed
```

## Change output

You may specify the output file using `-o out.json` option:

```bash
$ wasc data/example_websites.csv -o out.json
Use default checkers
Analysis of 2 websites...
100%|███████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  4.30it/s]
Save results in out.json
Completed
```

## List checkers

The option `-l` gives the list of checkers that are known by Wasc.

```bash
$ wasc data/example_websites.csv -l         
AccessChecker
AccessLinkChecker
AccessRateChecker
ContactLinkChecker
DoctypeChecker
FooterChecker
HeaderChecker
HeadLvlChecker
HeadNbChecker
LangChecker
LegalChecker
```
The list of available checkers is also given in page [Checkers](checkers.md) with their description.
## Change checkers

To use your list of checkers, simply put the list in a file and give it through option `-c`.
An example is given in `data/checkers.csv`.

In the CSV file, checkers are simply listed on a single column without header
```
AccessChecker
AccessLinkChecker
AccessRateChecker
```

Example of `-c` option:

```bash
$ wasc data/example_websites.csv -c data/checkers.csv 
Read checkers from data/checkers.csv
Analysis of 2 websites...
100%|███████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  5.45it/s]
Results:
{
    "Design Gouv": {
        "Erreur": "",
        "Lien accessibilité": "https://design.numerique.gouv.fr/misc/accessibilite",
        "Mention accessibilité": "totalement conforme",
        "Taux d'accessibilité": "100%",
        "URL": "https://design.numerique.gouv.fr/"
    },
    "Example": {
        "Erreur": "",
        "Lien accessibilité": "échec",
        "Mention accessibilité": "échec",
        "Taux d'accessibilité": "échec",
        "URL": "http://example.com/"
    }
}
Completed
```
