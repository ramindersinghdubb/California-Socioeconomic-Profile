"""
Interface for retrieving the options for submeasures.
"""

import typing as t

from dash import html



class SubmeasureInterface:
    """
    Interface for retrieving options for the submeasure dropdown.
    """

    @classmethod
    def get_submeasure_options(cls, topic: str) -> t.List[t.Dict[str, t.Any]]:
        """
        Retrieve the list of submeasure options for the indicated topic/measure.

        Parameters
        ----------
        topic
            One of the developer-specified topics listed in the metadata
            YAML configuration file.

            See `cls._dict_lambda`.
        """
        options = cls._dict_lambda()[topic]()
        return options

    @classmethod
    def _dict_lambda(cls) -> dict[str, t.Callable[[], dict[str, t.Any]]]:
        return {
            'Contract Rent': cls._submeasure_options_ContractRent,
            'Economic Measures': cls._submeasure_options_EconomicMeasures,
            'Education': cls._submeasure_options_Education,
            'Employment Statistics': cls._submeasure_options_EmploymentStatistics,
            'Food Stamps': cls._submeasure_options_FoodStamps,
            'Health Insurance Coverage': cls._submeasure_options_HealthInsuranceCoverage,
            'Household Income': cls._submeasure_options_HouseholdIncome,
            'Housing Units and Occupancy': cls._submeasure_options_HousingUnitsandOccupancy,
            'Population': cls._submeasure_options_Population,
            'Poverty': cls._submeasure_options_Poverty,
            'Rent Burden': cls._submeasure_options_RentBurden,
            'Transportation Methods to Work': cls._submeasure_options_TransportationMethodstoWork,
            'Work Hours': cls._submeasure_options_WorkHours
        }
    
    @classmethod
    def _submeasure_options_ContractRent(cls):
        submeasures = [
            'Distribution of Contract Rents'
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_EconomicMeasures(cls):
        submeasures = [
            'Civilian Workforce by Industry',
            'Civilian Workforce by Occupation',
            'Civilian Workforce by Sector',
            # 'Median Earnings, All Workers by Industry',
            # 'Median Earnings, Full-Time Workers by Industry',
            # 'Gender Pay Gap, All Workers',
            # 'Gender Pay Gap, Full-Time Workers',
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_Education(cls):
        submeasures = [
            # 'Educational Attainment by Citizenship Status',
            'Educational Attainment by Racial Status',
            'Educational Attainment by Age',
            'Educational Attainment by Sexual Orientation'
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_EmploymentStatistics(cls):
        submeasures = [
            'Unemploy. Rate by Racial Status',
            'LFPR by Racial Status',
            'EPOP Ratio by Racial Status',
            'Unemploy. Rate by Sexual Orientation',
            'LFPR by Sexual Orientation',
            'EPOP Ratio by Sexual Orientation',
            'Unemploy. Rate by Educational Attainment',
            'LFPR by Educational Attainment',
            'EPOP Ratio by Educational Attainment',
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_FoodStamps(cls):
        submeasures = [
            'Food Stamps Recipiency by Racial Status',
            'Food Stamps Recipiency by Poverty Status',
            'Food Stamps Recipiency by Disability Status',
            'Food Stamps Recipiency by Working Status',
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_HealthInsuranceCoverage(cls):
        submeasures = [
            'Uninsured Individuals by Racial Status',
            'Uninsured Individuals by Sexual Orientation',
            'Uninsured Individuals by Citizenship Status',
            'Uninsured Individuals by Educational Attainment',
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_HouseholdIncome(cls):
        submeasures = [
            'Income Distribution',
            # 'Income Distribution (Families)',
            # 'Income Distribution (Married Couples)',
            # 'Income Distribution (Nonfamily Households)',
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_HousingUnitsandOccupancy(cls):
        submeasures = [
            'Property Values for Owner-Occupied Units',
            # 'Occupancy by Householder Racial Status',
            # 'Occupancy by Householder Age',
            # 'Housing Units by Year Built',
            'Rooms in Housing Units',
            'Bedrooms in Housing Units',
            'House Heating Fuel',
            'Select Units Lacking Facilities',
            'Occupants Per Room',
            'Monthly Owner Costs for Units w/ Mortgage',
            # 'Year Householder Moved In'
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_Population(cls):
        submeasures = [
            'Population by Age',
            'Population by Racial Status',
            'Population by Sexual Orientation'
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_Poverty(cls):
        submeasures = [
            'Poverty Status by Racial Status',
            'Poverty Status by Sexual Orientation',
            'Poverty Status by Age',
            'Poverty Status by Employment Status',
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_RentBurden(cls):
        submeasures = [
            'Rent Burden and Severe Rent Burden',
            'Rent Burden by Age',
            'Rent Burden by Income'
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_TransportationMethodstoWork(cls):
        submeasures = [
            'Commute Methods to Work',
            'Departure Times',
            'Travel Times',
            'Vehicles Available'
        ]
        options = cls.__create_options(submeasures)
        return options

    @classmethod
    def _submeasure_options_WorkHours(cls):
        submeasures = [
            'Usual Hours Worked Weekly',
            'Average Hours Worked Weekly',
        ]
        options = cls.__create_options(submeasures)
        return options


    @classmethod
    def __create_options(cls, list_of_submeasures: t.List[str]) -> t.List[t.Dict[str, t.Any]]:
        options = [
            {
                'label': html.Span(children = [i], style = {'color': '#000000'}),
                'value': i,
            } for i in list_of_submeasures
        ]
        return options