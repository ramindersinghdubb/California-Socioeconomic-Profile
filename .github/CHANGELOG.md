# CHANGELOG

## Version 0.1.2

### June 29, 2026

#### Features

Consistent with the prospective developments stated in version 0.1.1, the following features have been incorporated.

- **Submeasure dropdown**
    - Function: To permit the user greater luxury over the entire breadth of data a specific data table has to offer

- **Data download option**
    - Function: To permit end-users/developers to cross-reference the data employed as part of the app

#### Bugs

- [`app.py`, lines 203-227](../app.py)
    - A bug appears wherein the user, having selected a value from the submeasure dropdown, will be shown the hoverinfo if any of the other dropdowns beside the submeasure dropdown.
    - For the time being, we supply the submeasure value as its own input in the choropleth figure callback, albeit at the slight drawback that the figure refreshes every time any one of the dropdown selections have been modified even though the underlying data does not change if a submeasure is selected.

#### Notes

There are particular submeasures that may not necessarily be captured in certain years, owing to various and unforeseen changes to the Census Bureau survey and data tabulation methodology. As such, to mitigate the higher degree of complexity incurred from cross-checking year support and submeasure availability, alongside reviewing the obvious annual revisions for consistency, it has been decided to only display that information which has been *consistently* been made available (in one form or the other) from the onset of each Census Bureau dataset.

For instance, of noteworthy importance is the introduction of median earnings information and median gender earnings pay gap information starting 2015 with the American Community Survey S2413 "Industry By Sex And Median Earnings In The Past 12 Months" Subject Table dataset. However, the general category to which it subscribes in the current iteration, "Economic Measures", has a calendar year support starting as early as 2009 (see [`../config/dropdown_config.json`](../config/dropdown_config.json)). Nonetheless, this information can be re-presented as its own standalone measure (as opposed to a submeasure) and benefit directly from the existing implementation of dropdown configuration settings. That said, the current implementation has not reorganized accordingly (this will be explored and potentially implemented prior to the version 1.0 implementation).

Likewise, some data label information changes drastically over the years as to evade any deterministic rule. For instance, the American Community Survey DP04 "Selected Housing Characteristics" Detailed Profile Table dataset indicates a set of information pertaining to the calendar year a householder moves into their housing unit. This information understandably changes, and the Census Bureau correctly makes the assesment to revise their variable labels to track this information. However, absent a (rather strained) annual revision, this necessarily impedes a simple deterministic rule.

For these reasons, it is incumbent on the end-user, who may be interested in visualizations beyond presently provided, to make use of the data (accessed via data download feature) as they see fit. It is hoped that the regular and maintanenced ingestion pipeline (cf. [`../ingestion/`](../ingestion/)) serves further purpose and motivation for such users.


## Version 0.1.1

### June 17, 2026

#### Fixes

- `dash` 4.0 and higher has a [known bug](https://community.plotly.com/t/inconsistent-dropdown-focus-behaviour-in-4-0/96516) where users interacting with searchable `dash.dcc.Dropdown` elements may be forced out after typing a character. As such, this project downgrades to the stable 3.2.0 version of `dash`.
    - An unfortunate consequence is the search property is placed in the dropdown selection itself, as opposed to being its own component in the set of options. Compare the version 4.0 search (picture below) to the 3.2.0 version search (gif below).

[<img src="./issues/dash_dropdown_v4.png" alt="Dash 4.0 search">](./issues/dash_dropdown_v4.png)

![<img src="./issues/dash_dropdown_v3_2.gif" alt="Dash 3.2.0 search">](./issues/dash_dropdown_v3_2.gif)


#### In-Development

-  *Submeasure dropdown*
    - Purpose: To permit the user greater luxury over the entire breadth of data a specific data table has to offer

- *Data download option*
    - Purpose: To permit end-users/developers to cross-reference the data employed as part of the app