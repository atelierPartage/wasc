## Upgrading
To upgrade Wasc to the latest version, use pip:

`pip install -U wasc`

You can determine your currently installed version using:

```bash
$ wasc --version
wasc, version 1.0.0
```

## Maintenance team
The current and past members of the wasc team.

[@gcollet](https://github.com/gcollet)

## Version 1.0.0 (2023-07-12)
* 11 checkers available (docs are updated)
* Use trafilatura parallel download of webpages
* Better accessibility link and rate detection
* Bugfix: Better URL management with urllib.urljoin
* Bugfix: Use trafilatura extract feature for accessibility rate detection
## Version 0.4.0 (2023-07-10)
* Use trafilatura instead of requests to download webpages -> this allows to use simple parallel downloads
* Moreover, trafilatura extract text and will be usefull for text searching
* New checkers: 
    * HeaderChecker: detects <header> tag
    * FooterChecker: detects <footer> tag
    * AccessRateChecker: finds the accessibility rate in accessibility statement
    * ContactLinkChecker: finds a contact link in the page (with keywords "contact" and "ecrire")
* Bugfix: Correction of url concatenation when sub path is given in href
## Version 0.3.0 (2023-07-05)
* Major code simplication by removing two classes Criterion and Report that are useless
* The main function only store results in lists that are used to initiate a DataFrame
* This simplification may allow parallel analyses
* Bugfix: use pandas DataFrame to correctly export results in CSV

## Version 0.2.0 (2023-07-03)
* Include `pandas` to simplify CSV reading/writing (and for future production of dataframe through API)
* Change default output message on stdout
* json and csv format are available

## Version 0.1.2 (2023-07-01)
* Test a progress bar based on the number of websites (tqdm package)
* Default criteria are:
    * Accessibilité : `AccessChecker`, `AccessLinkChecker`
    * Mentions légales : `MentionsLegalesChecker`
* Add tests for checkers :
    * `LangChecker`
    * `DoctypeChecker`
    * `AccessChecker`
    * `AccessLinkChecker`
    * `MentionsLegalesChecker`
* json format is available
* Modify project.toml to integrated `coverage` during tests
* Bugfix: Changed names of checker to be more explicit : `DFTT04Checker` -> `AccessChecker`
* Bugfix: Correct github project url
* Bugfix: Better management of ReadTimeout error in `report.py`
## Version 0.1.1 (2023-06-28)

* Changed name to `wasc`
* Removed old checker name `flb`to `default`

## Version 0.0.1 (2023-06-07)

Minimum viable first version with checkers from Juliette Francis.
Still the old name waccess, will change in next version