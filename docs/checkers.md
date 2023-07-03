# Checkers

Wasc contains already defined checkers in `default_chekers.py`.

All checkers return `"échec"` on failure.

Default checkers are listed below with their definition.

## `DoctypeChecker`
* Rule: the HTML document contains `<!DOCTYPE html>`
* Rule: `<!DOCTYPE html>` is before `<html>`
* Return: `html`

## `LangChecker`
* Rule: `<html>` has an attribute `lang`
* Return: the value of `lang`

## `LegalChecker`
* Rule: `"Mentions légales"` exists somewhere in the page
* Rule: `"Mentions légales"` is a link `<a>` with attribute `href`
* Return: the value of `href`

## `AccessChecker`
* Rule: `"Accessibilité : XX conforme"` exists somewhere in the page with `XX` in `["non", "partiellement", "totalement"]`
* Return: `XX conforme`

## `AccessLinkChecker`
* Rule: if `AccessChecker` is valid, then if it's a link
* Rule: if the previous rule fails, check each link in the page looking for keyword `accessibilite` at the end of URL
* Return: the value of the link

## `AccessRateChecker` (Todo)
* Rule: if `AccessLinkChecker` is valid, get the page from the link. In this page, an accessibility rate is given as percent
* Return: the accessibility rate