Wasc contains already defined checkers in `chekers.py`.

All checkers return `"échec"` on failure.

Available checkers are listed below with their definition.

- [`AccessChecker`](#accesschecker)
- [`AccessLinkChecker`](#accesslinkchecker)
- [`AccessRateChecker`](#accessratechecker)
- [`ContactLinkChecker`](#contactlinkchecker)
- [`DoctypeChecker`](#doctypechecker)
- [`FooterChecker`](#footerchecker)
- [`HeaderChecker`](#headerchecker)
- [`HeadLvlChecker`](#headlvlchecker)
- [`HeaderNbChecker`](#headernbchecker)
- [`LangChecker`](#langchecker)
- [`LegalChecker`](#legalchecker)

## `AccessChecker`
* Rule: `"Accessibilité : XX conforme"` exists in the page with `XX` in `["non", "partiellement", "totalement"]`
* Rule: Search in `<footer>`, then `<div id="footer>`, then the whole page
* Return: `XX conforme`

## `AccessLinkChecker`
* Rule: if `AccessChecker` is valid and it's a link returns it
* Rule: if the previous rule fails, check each link in the page looking `accessibilit` in the text inside `<a>`
* Rule: if the previous rule fails, check each link in the page looking `accessibilit` in the `href` attribute
* Return: the link url

## `AccessRateChecker`
* Rule: if `AccessLinkChecker` is valid, get the page from the link.
* Rule: the accessibility rate is in a tag containing "conformité" and a floating number directly followed by '%'
* Return: the accessibility rate

## `ContactLinkChecker`
* Rule: Finds `contact` or `ecrire` in a link `<a>` tag
* Return: the link url

## `DoctypeChecker`
* Rule: the HTML document contains `<!DOCTYPE html>`
* Rule: `<!DOCTYPE html>` is before `<html>`
* Return: `html`

## `FooterChecker`
* Rule: the HTML document contains `<footer>`
* Return: `présent` if the tag is found, else `échec`

## `HeaderChecker`
* Rule: the HTML document contains `<header>`
* Return: `présent` if the tag is found, else `échec`

## `HeadLvlChecker`
* Rule: For each `<head>` tags in the page, calculate its depth
* Return: the list of depth of `<head>` tags 

## `HeaderNbChecker`
* Rule: the HTML document contains `<head>`
* Return: the number of `<head>` tags present on the page

## `LangChecker`
* Rule: `<html>` has an attribute `lang`
* Return: the value of `lang`

## `LegalChecker`
* Rule: `"Mentions légales"` exists somewhere in the page
* Rule: `"Mentions légales"` is a link `<a>` with attribute `href`
* Return: the value of `href`

