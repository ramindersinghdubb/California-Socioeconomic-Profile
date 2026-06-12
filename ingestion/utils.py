"""
Smaller callables/functions.
"""
import unicodedata

import pandas as pd


def lettered_table(
    table: str,
    first_letter: str = 'A',
    last_letter: str = 'I'
) -> list[str]:
    """
    For cases when the Census Bureau has certain tables decomposed by
    variants (usually in the case of tables denoted by racial marker).
    
    We exploit the fact that these variants are aligned in a sequence,
    starting from `"$TABLE"first_letter` to `"$TABLE"last_letter` (e.g.
    the ACS 5-Year Detailed Table B22005 'Receipt of Food Stamps/SNAP'
    dataset is decomposed across self-identified racial markers, B22005A
    to B25005I).

    Parameters
    ----------
    table
        The Census Bureau table.

    first_letter
        The first letter/variant. Typically 'A'.

    last_letter
        The last letter/variant. Typically 'I'.

    Returns
    -------
    A list of strings designating the entire collection of variants
    for a given table.
    """
    return [table + chr(i) for i in range(ord(first_letter), ord(last_letter) + 1)]



def remove_accents(input_str: str) -> str:
    """
    Return the non-accented ASCII string for the inputed string.
    """
    
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('ASCII')



def append_counties_to_cities(
    city_series: pd.Series, county_series: pd.Series
) -> pd.Series:
    """
    If a place name has duplicate entries anywhere, append each entry's
    county name to any instance of the place name.
    """
    dummy_series = city_series.str.replace(' ', '').str.lower()
    counts = dummy_series.value_counts()
    for item in counts.index:
        if counts[item] > 1:
            city_series[dummy_series == item] += ' (' + county_series[dummy_series == item] + ')'
    return city_series



def get_california_fips_df() -> pd.DataFrame:
    """
    Retrieve the Cali city/place `pandas.DataFrame`.

    The columns are:
        - `GEO_ID`: FIPS codes for each place,

        - `PLACENAME`: The unique city/place names,

        - `COUNTIES`: Each city/place's corresponding county
    """
    url = "https://www2.census.gov/geo/docs/reference/codes2020/place/st06_ca_place2020.txt"

    df = pd.read_csv(url, sep='|', dtype = {'STATEFP': object, 'PLACEFP': object})
    df['GEO_ID'] = df['STATEFP'] + df['PLACEFP']
    df = df[['GEO_ID', 'PLACENAME', 'COUNTIES']]

    df['PLACENAME'] = df['PLACENAME'].str.replace(' CDP', "") \
        .str.replace(' city', "") \
        .str.replace(' town', " Town") \
        .apply(remove_accents)
    df['PLACENAME'] = append_counties_to_cities(df['PLACENAME'], df['COUNTIES'])

    return df