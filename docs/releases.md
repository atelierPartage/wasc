## Upgrading
To upgrade Wasc to the latest version, use pip:

`pip install -U wasc`

You can determine your currently installed version using:

```bash
$ wasc --version
wasc, version 0.2.0
```

## Maintenance team
The current and past members of the wasc team.

[@gcollet](https://github.com/gcollet)

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