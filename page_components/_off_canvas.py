"""
Display of and styling for the off-canvas text.
"""
import typing as t

from dash import html

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components.config import CONFIG_SETTINGS



class OffCanvasText:
    """
    Interface for the off-canvas help text.
    """
    @classmethod
    def get_help_text(cls, topic: str) -> html.Div:
        """
        Retrieve the :py:class:`dash.html.Div` component.

        This component is used to display the help text in the off-canvas
        body (triggered when users interact with the relevant button) for
        the selected topic.

        Parameters
        ----------
        topic
            One of the developer-specified topics listed in the metadata
            YAML configuration file.

            See `cls._dict_lambda`.
        """
        help_content = cls._help_text_topic(topic)
        foonote_content = cls._footnote_text()
        text    = html.Div(
            children = [
                *help_content,
                *foonote_content
            ]
        )

        return text
    

    @classmethod
    def _footnote_text(cls) -> list:
        footnote_title = html.Span(
            className = 'off-canvas-title-text',
            children  = ["Notes"]
        )

        footnote_body = [
            html.Span(
                "All data presented here were taken from the American Community Survey "
                "5-Year Estimate data ("
            ),
            html.A(
                "link",
                href = 'https://www.census.gov/data/developers/data-sets/acs-5year.html'
            ),
            html.Span(
                "). Data is presented at the census-tract level. This tool is not affiliated "
                "with, nor endorsed by, the government of the United States. Survey data is "
                "based on individuals’ voluntary participation in questionnaires. The creator "
                "is not liable for any missing, inaccurate, or incorrect data."
            )
        ]

        footnote = [
            footnote_title,
            html.Br(),
            *footnote_body
        ]
        return footnote
    
    @classmethod
    def _help_text_topic(cls, topic: str) -> list:
        topic_func = cls._dict_lambda()[topic]
        title = html.Span(
            className = 'off-canvas-title-text',
            children  = [topic]
        )
        body, references = topic_func()

        content = [
            title,
            html.Br(),
            *body,
            html.Br(),
            *references,
            html.Br(),
        ]

        return content


    @classmethod
    def _dict_lambda(cls) -> dict[str, t.Callable[[], tuple[list, list]]]:
        return {
            'Contract Rent': cls._help_text_ContractRent,
            'Economic Measures': cls._help_text_EconomicMeasures,
            'Education': cls._help_text_Education,
            'Employment Statistics': cls._help_text_EmploymentStatistics,
            'Food Stamps': cls._help_text_FoodStamps,
            'Health Insurance Coverage': cls._help_text_HealthInsuranceCoverage,
            'Household Income': cls._help_text_HouseholdIncome,
            'Housing Units and Occupancy': cls._help_text_HousingUnitsandOccupancy,
            'Population': cls._help_text_Population,
            'Poverty': cls._help_text_Poverty,
            'Rent Burden': cls._help_text_RentBurden,
            'Transportation Methods to Work': cls._help_text_TransportationMethodstoWork,
            'Work Hours': cls._help_text_WorkHours
        }


    @classmethod
    def _help_text_ContractRent(cls) -> tuple[list, list]:
        body = [
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Contract rent'
            ),
            html.Span(
                ' is defined as '
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = """
                the monthly rent agreed to or contracted for, regardless of any furnishings,
                utilities, fees, meals, or services that may be included (United States
                Census Bureau, 2024).
                """
            )
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_EconomicMeasures(cls) -> tuple[list, list]:
        body = [
            html.Span(
                children = """
                Estimates are reported for the civilian, 16 and older employed labor force. 
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Industry'
            ),
            html.Span(
                children = """
                 refers to the particular sphere of trade a civilian worker is employed in. 
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Occupation'
            ),
            html.Span(
                children = """
                 relates to the services associated with a civilian worker's employment. 
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Sector'
            ),
            html.Span(
                children = """
                 refers to the relative jurisdiction under which a civilian worker's employment is conducted (i.e.
                'private-sector', 'public-sector', self-employed, and family work).
                """
            )
        ]

        source = [
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_Education(cls) -> tuple[list, list]:
        body = [
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Educational attainment'
            ),
            html.Span(
                ", unless otherwise stated, is reported for the 25 year and older population."
            ),
            html.Br(),
            html.Br(),
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_EmploymentStatistics(cls) -> tuple[list, list]:
        body = [
            html.Span(
                "The "
            ),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'unemployment rate'
            ),
            html.Span(
                """
                 is defined as the proportion of persons in the labor force who did not work in the 
                reference period  under question but were actively searching for work during the 
                reference period in question.
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                "The "
            ),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'labor force participation rate'
            ),
            html.Span(
                """
                 is defined as the proportion of working-aged (16 and older) persons who are
                working or actively searching for work.
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                "The "
            ),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'employment-to-population ratio'
            ),
            html.Span(
                """
                 is defined as the proportion of working-aged (16 and older) persons who are
                working.
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                """
                Per the 2024 American Community Survey Design & Methodology Report, questions
                regarding labor force status are designed to identify the following:
                """
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = html.Ol(
                    children = [
                        html.Li(
                            className = 'off-canvas-source-orderedlist-item',
                            children  = [
                                html.Span(
                                    """
                                    People who worked at any time during the reference week;
                                    """
                                ),
                            ]
                        ),
                        html.Li(
                            className = 'off-canvas-source-orderedlist-item',
                            children  = [
                                html.Span(
                                    """
                                    People on temporary layoff who were available for work;
                                    """
                                ),
                            ]
                        ),
                        html.Li(
                            className = 'off-canvas-source-orderedlist-item',
                            children  = [
                                html.Span(
                                    """
                                    People who did not work during the reference week but who
                                    had jobs or businesses from which they were temporarily
                                    absent (excluding layoffs);
                                    """
                                ),
                            ]
                        ),
                        html.Li(
                            className = 'off-canvas-source-orderedlist-item',
                            children  = [
                                html.Span(
                                    """
                                    People who did not work but were available during the
                                    reference week, and who were looking for work during the
                                    last four weeks; and
                                    """
                                ),
                            ]
                        ),
                        html.Li(
                            className = 'off-canvas-source-orderedlist-item',
                            children  = [
                                html.Span(
                                    """
                                    People not in the labor force.
                                    """
                                ),
                            ]
                        )
                    ]
                )
            )
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_FoodStamps(cls) -> tuple[list, list]:
        body = [
            html.Span(
                children = "Per the 2024 American Community Survey Design and Methodology Report, "
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = [
                    html.Span(
                        """
                        the Food and Nutrition Service of the U.S. Department of Agriculture (USDA) administers the 
                        """
                    ),
                    html.Span(
                        className = 'off-canvas-vocab',
                        children  = 'Supplemental Nutrition Assistance (Food Stamp) Program (SNAP)'
                    ),
                    html.Span(
                        """
                         through state and local welfare offices. This program is the major national income-support 
                        program for which all low-income and low-resource households, regardless of household 
                        characteristics, are eligible. This question asks if anyone in the households received SNAP 
                        benefits at any time during the 12-month period before the [American Community Survey] 
                        interview (United States Census Bureau, 2024).
                        """
                    ),
                ]
            )
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_HealthInsuranceCoverage(cls) -> tuple[list, list]:
        body = [
            html.Span(
                'Per the 2024 American Community Survey Design and Methodology Report, '
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = """
                [the insured and uninsured population is assessed] by asking about coverage through 
                an employer, direct purchase from an insurance company, Medicare, Medicaid or 
                other government-assistance health plans, military health care, Veterans Affairs 
                health care, Indian Health Service, or other types of health insurance or coverage 
                plans. Plans that cover only one type of health care (such as dental plans) or plans 
                that only cover a person in case of an accident or disability are not included (United 
                States Census Bureau, 2024).
                """
            )
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_HouseholdIncome(cls) -> tuple[list, list]:
        body = [
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Income'
            ),
            html.Span(
                ' is defined as '
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = """
                the sum of the amounts reported separately for wage or salary income; net self-employment 
                income; interest, dividends, or net rental or royalty income, or income from estates and 
                trusts; social security or railroad retirement income; Supplemental Security Income; public 
                assistance or welfare payments; retirement, survivor, or disability pensions; and all other 
                income. Income is reported for the past 12 months from the date of the interview. The 
                estimates are inflation-adjusted using the Consumer Price Index (United States Census Bureau, 
                2024).
                """
            ),
            html.Br(),
            html.Span(
                f"""
                To adjust for changes in cost of living, adjustment to the Consumer Price Index ("constant 
                dollars") was conducted for data years earlier than {max(CONFIG_SETTINGS['YEARS'])} through the
                """
            ),
            html.A(
                "Bureau of Labor Statistics Consumer Price Index Research Retroactive Series (R-CPI-U-RS)",
                href = "https://www.bls.gov/cpi/research-series/r-cpi-u-rs-home.htm"
            ),
            html.Span(
                " series."
            ),
            html.Br(),
            html.Br()
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology". 
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    ),
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2025. "Current versus Constant (or Real)
                                Dollars". 
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www.census.gov/topics/income-poverty/income/guidance/current-vs-constant-dollars.html'
                            )
                        ]
                    ),
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Bureau of Labor Statistics. 2021. "Consumer Price Index Research 
                                Retroactive Series (R-CPI-U-RS)". 
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www.bls.gov/cpi/research-series/r-cpi-u-rs-home.htm'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_HousingUnitsandOccupancy(cls) -> tuple[list, list]:
        body = [
            html.Span(
                'The reference person, or '
            ),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'householder'
            ),
            html.Span(
                ", is usually "
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = """
                the person, or one of the people, in whose name the home is owned, being bought, 
                or rented and who is listed as 'Person 1' on the survey questionnaire. If there 
                is no such person in the household, any adult household member 15 and older can 
                be designated (United States Census Bureau, 2024).
                """
            ),
            html.Span(
                'The '
            ),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'property value'
            ),
            html.Span(
                ' is computed based on '
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = """
                the respondent’s estimate of how much the property (house and lot, mobile home and 
                lot, or condominium unit) would sell for. The information is collected for [housing 
                units] that are owned or being bought and for vacant [housing units] that are for 
                sale. If the house or mobile home is owned or being bought, but the land on which 
                it sits is not, the respondent is asked to estimate the combined value of the house 
                or mobile home and the land. For vacant [housing units], value is defined as the 
                price asked for the property. This information is obtained from real estate agents, 
                property managers, or neighbors (ibis.).
                """
            )
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_Population(cls) -> tuple[list, list]:
        body = [
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Race'
            ),
            html.Span(
                """
                 refers to the socio-political category that individuals report themselves as. Note 
                that race is not rooted in science or biology. For instance, the fact that 'Black' 
                (a color) and 'Asian' (a geographical point of reference) reflect popular contemporary 
                understandings of race and racial taxonomies within the United States metropole are 
                in no way symptomatic of any scientific consensus. Further, note too the vagueness of 
                'Asian': could it refer to individuals hailing from Iran just as much as others hailing 
                from Laos, given their respective landmasses are located within the Asian continent, or 
                does 'Asian' refer to a popular understanding of individuals from landmasses close to 
                and/or bordering the eastern Pacific seaboard?
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                """
                For these, and other reasons, population estimates segmented by race should instead be 
                motivated by a socio-political-economic understanding of the ways in which certain peoples 
                who have understood themselves distinctively as a community (or, loosely, "population") 
                have come to be situated.
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                """
                For purposes of demonstration, Punjab is taken as a point of reference. In what ways has 
                im/migration policy affected the presence of members of the Punjabi community? How has 
                economic precarity in Punjab affected Punjabi individuals situated along the metropole 
                and their relationships with both Punjab and the metropole? In what ways have existing 
                community groups and structures (e.g. gurdwaras) made certain places amenable to Punjabi 
                folk and the making of the Punjabi community? How have legal demarcations and borders 
                help to delineate a colloquial understanding of Charhda Punjab?
                """
            ),
        ]

        source = []

        return body, source


    @classmethod
    def _help_text_Poverty(cls) -> tuple[list, list]:
        body = [
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Poverty'
            ),
            html.Span(
                """
                 is not a directly asked question in the American Community Survey but formulated 
                indirectly with the assistance of information regarding respondents' income and 
                household composition (United States Census Bureau, 2024).
                """
            ),
            html.Br(),
            html.Br()
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_RentBurden(cls) -> tuple[list, list]:
        body = [
            html.Span(
                "Renters who are "
            ),
            html.Span(
                className = 'off-canvas-critical',
                children  = 'rent-burdened'
            ),
            html.Span(
                " pay "
            ),
            html.Span(
                className = 'off-canvas-critical',
                children  = 'over 30%'
            ),
            html.Span(
                " of their household income to rent. Renters who are "
            ),
            html.Span(
                className = 'off-canvas-critical',
                children  = 'severely rent-burdened'
            ),
            html.Span(
                " pay "
            ),
            html.Span(
                className = 'off-canvas-critical',
                children  = 'over 50%'
            ),
            html.Span(
                """
                 of their household income to rent. Rent burden and severe rent burden 
                is found by taking the percentage of household income going to gross rent. 
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Gross rent'
            ),
            html.Span(
                " is defined as"
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = """
                [the monthly rent agreed to or contracted for, regardless of any furnishings, 
                utilities, fees, meals, or services that may be included] plus the estimated 
                average monthly cost of utilities and fuels, if these are paid by the renter 
                (United States Census Bureau, 2024).
                """
            )
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_TransportationMethodstoWork(cls) -> tuple[list, list]:
        body = [
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Commute methods to work'
            ),
            html.Span(
                """
                 refer to "the principal mode of travel or type of conveyance that the 
                worker usually used to get from home to work during the reference week" 
                (United States Census Bureau, 2024). 
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Departure times'
            ),
            html.Span(
                """
                 refer to "the time of day that the respondent usually left home to go 
                to work during the reference week" (ibis.).
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Travel times'
            ),
            html.Span(
                """
                 to work refer to the number of minutes it usually takes the respondent to 
                get from home to work during the reference week (ibis.).
                """
            ),
            html.Br(),
            html.Br(),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'Vehicles available'
            ),
            html.Span(
                " show"
            ),
            html.Blockquote(
                className = 'off-canvas-block-quote',
                children  = """
                the number of passenger cars, vans, and pickup or panel trucks of one-ton 
                capacity or less kept at home and available for the use of household members. 
                Vehicles rented or leased for one month or more, company vehicles, and police 
                and government vehicles are included if kept at home and used for nonbusiness 
                purposes. Dismantled or immobile vehicles are excluded, as are vehicles kept 
                at home but used only for business purposes (ibis.). 
                """
            )
        ]


        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source


    @classmethod
    def _help_text_WorkHours(cls) -> tuple[list, list]:
        body = [
            html.Span(
                "Estimates for "
            ),
            html.Span(
                className = 'off-canvas-vocab',
                children  = 'usual hours worked weekly'
            ),
            html.Span(
                " are reported for the civilian, 16 and older employed labor force."
            ),
            html.Br(),
            html.Br()
        ]

        source = [
            html.Span(
                className = 'off-canvas-title-text',
                children  = ['Sources']
            ),
            html.Ul(
                className = 'off-canvas-source-list',
                children  = [
                    html.Li(
                        className = 'off-canvas-source-list-item',
                        children  = [
                            html.Span(
                                """
                                United States Census Bureau. 2024. "American Community Survey
                                and Puerto Rico Community Survey Design and Methodology".
                                """
                            ),
                            html.A(
                                "Link.",
                                href = 'https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'
                            )
                        ]
                    )
                ]
            )
        ]

        return body, source
