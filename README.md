# GOOGLE SCHOLAR SCRAPER

Simple scraper which let user extract data on citations and coauthors in recursive manner from Google Scholar (further acronym GS will be used).

Main concepts:

`scholars`: list of sets with GS ids, `scholars[0]` is initial set (1st level of search), `scholars[1]` (2nd level of search) is set of coauthors of scholars from `scholars[0]`, `scholar[2]` is set of coauthors of scholars from `scholars[1]` and so on.

`search_deepness`: integer that determines how many levels would be in the current search.

`coauthors`: set of GS ids for all the coauthors found on current level of search, in the end of the level loop `coauthors` are appended to `scholars` list.
