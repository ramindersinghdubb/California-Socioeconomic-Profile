"""
Submeasures options.

The current implementation is clunky but, in a future update
with hosting via cloud services, this will be re-formatted.
(TODO)
"""

from dash import html


submeasures_dict = dict()
    


# -- Contract Rent -- #
dummy_labels_list = ['Distribution of Contract Rents',
                     'Contract Rents Over Time'
                    ]
dummy_values_list = ['ContractRent_LONG',
                     'ContractRent_TIME'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Contract Rent'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Rent Burden -- #
dummy_labels_list = ['Rent/Severe Rent Burden Over Time', 'Rent Burden and Severe Rent Burden',
                     'Rent Burden by Age (Over Time)', 'Rent Burden by Age',
                     'Rent Burden by Income (Over Time)', 'Rent Burden by Income',
                    ]
dummy_values_list = ['RentBurden_TIME', 'RentBurden_LONG',
                     'RentBurden_AGE_TIME', 'RentBurden_AGE_LONG',
                     'RentBurden_INCOME_TIME', 'RentBurden_INCOME_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Rent Burden'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Employment Statistics -- #
dummy_labels_list = ['Unemp. Rate by Race (Over Time)', 'Unemployment Rate by Race',
                     'LFPR by Race (Over Time)', 'LFPR by Race',
                     'EPOP by Race (Over Time)', 'EPOP by Race',
                     'Unemp. Rate by Sex (Over Time)', 'Unemployment Rate by Sex',
                     'LFPR by Sex (Over Time)', 'LFPR by Sex',
                     'EPOP by Sex (Over Time)', 'EPOP by Sex',
                     'Unemp. Rate by Education (Over Time)', 'Unemployment Rate by Education',
                     'LFPR by Education (Over Time)', 'LFPR by Education',
                     'EPOP by Education (Over Time)', 'EPOP by Education',
                    ]
dummy_values_list = ['EmploymentStatistics_UNEMP_RACE_TIME', 'EmploymentStatistics_UNEMP_RACE_LONG',
                     'EmploymentStatistics_LFPR_RACE_TIME', 'EmploymentStatistics_LFPR_RACE_LONG',
                     'EmploymentStatistics_EPOP_RACE_TIME', 'EmploymentStatistics_EPOP_RACE_LONG',
                     'EmploymentStatistics_UNEMP_SEX_TIME', 'EmploymentStatistics_UNEMP_SEX_LONG',
                     'EmploymentStatistics_LFPR_SEX_TIME', 'EmploymentStatistics_LFPR_SEX_LONG',
                     'EmploymentStatistics_EPOP_SEX_TIME', 'EmploymentStatistics_EPOP_SEX_LONG',
                     'EmploymentStatistics_UNEMP_EDUCATIONALSTATUS_TIME', 'EmploymentStatistics_UNEMP_EDUCATIONALSTATUS_LONG',
                     'EmploymentStatistics_LFPR_EDUCATIONALSTATUS_TIME', 'EmploymentStatistics_LFPR_EDUCATIONALSTATUS_LONG',
                     'EmploymentStatistics_EPOP_EDUCATIONALSTATUS_TIME', 'EmploymentStatistics_EPOP_EDUCATIONALSTATUS_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Employment Statistics'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Food Stamps -- #
dummy_labels_list = ['Food Stamps Recipients (by Race)',
                     'Food Stamps Recipients (by Poverty Status)',
                     'Food Stamps Recipients (by Disability Status)',
                     'Food Stamps Recipients (by Working Status)',
                    ]
dummy_values_list = ['FoodStamps_RACE_LONG',
                     'FoodStamps_POVERTY_LONG',
                     'FoodStamps_DISABILITYSTATUS_LONG',
                     'FoodStamps_WORKINGSTATUS_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Food Stamps'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Household Income -- #
dummy_labels_list = ['Income Distribution (for Households)',
                     'Income Distribution (for Families)',
                     'Income Distribution (for Married Couples)',
                     'Income Distribution (for Nonfamily Households)',
                    ]
dummy_values_list = ['HouseholdIncome_HOUSEHOLDS_LONG',
                     'HouseholdIncome_FAMILIES_LONG', 
                     'HouseholdIncome_MARRIEDCOUPLEFAMILIES_LONG',
                     'HouseholdIncome_NONFAMILYHOUSEHOLDS_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Household Income'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Housing Units and Occupancy -- #
dummy_labels_list = ['Home Values (Owner-Occupied Units)',
                     'Occupied Housing Units by Race',
                     'Occupied Housing Units by Age',
                     'Housing Units by Year Built',
                     'Rooms in Housing Units',
                     'Bedrooms in Housing Units',
                     'House Heating Fuel',
                     'Select Units Lacking Facilities',
                     'Occupants Per Room',
                     'Monthly Owner Costs for Units with Mortgage',
                     'Year Householder Moved In'
                    ]
dummy_values_list = ['HousingUnitsandOccupancy_HOMEVALUE_LONG',
                     'HousingUnitsandOccupancy_RACE_HOUSINGUNITS_LONG',
                     'HousingUnitsandOccupancy_AGE_HOUSINGUNITS_LONG',
                     'HousingUnitsandOccupancy_YEARBUILT_LONG',
                     'HousingUnitsandOccupancy_UNITROOMS_LONG',
                     'HousingUnitsandOccupancy_UNITBEDROOMS_LONG',
                     'HousingUnitsandOccupancy_HEATINGFUEL_LONG',
                     'HousingUnitsandOccupancy_LACKINGFACILITIES_LONG',
                     'HousingUnitsandOccupancy_OCCUPANTSPERROOM_LONG',
                     'HousingUnitsandOccupancy_MORTGAGESMOC_LONG',
                     'HousingUnitsandOccupancy_YEARMOVEDIN_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Housing Units and Occupancy'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]




# -- Poverty -- #
dummy_labels_list = ['Poverty by Race',
                     'Poverty by Sex (Coming Soon!)',
                     'Poverty by Age (Coming Soon!)',
                     'Poverty by Employment (Coming Soon!)',
                    ]
dummy_values_list = ['Poverty_RACE_LONG',
                     'Poverty_SEX_LONG',
                     'Poverty_AGE_LONG',
                     'Poverty_EMPLOYMENT_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Poverty'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

disabled_values = ['Poverty_SEX_LONG', 'Poverty_AGE_LONG', 'Poverty_EMPLOYMENT_LONG']
submeasures_dict['Poverty']  = [dict(item, **{'disabled': True}) if item['value'] in disabled_values else dict(item) for item in submeasures_dict['Poverty'] ]




# -- Health Insurance Coverage -- #
dummy_labels_list = ['Coverage by Race',
                     'Coverage by Sex (Coming Soon!)',
                     'Coverage by Citizenship Status (Coming Soon!)',
                     'Coverage by Educational Status (Coming Soon!)'
                    ]
dummy_values_list = ['HealthInsuranceCoverage_RACE_LONG',
                     'HealthInsuranceCoverage_SEX_LONG',
                     'HealthInsuranceCoverage_CITIZEN_LONG',
                     'HealthInsuranceCoverage_EDUCATIONALSTATUS_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Health Insurance Coverage'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

disabled_values = ['HealthInsuranceCoverage_CITIZEN_LONG', 'HealthInsuranceCoverage_SEX_LONG', 'HealthInsuranceCoverage_EDUCATIONALSTATUS_LONG']
submeasures_dict['Health Insurance Coverage']  = [dict(item, **{'disabled': True}) if item['value'] in disabled_values else dict(item) for item in submeasures_dict['Health Insurance Coverage'] ]




# -- Transportation Methods to Work -- #
dummy_labels_list = ['Commute Methods to Work',
                     'Departure Times',
                     'Travel Times',
                     'Vehicles Available'
                    ]
dummy_values_list = ['TransportationMethodstoWork_METHODSTOWORK_LONG',
                     'TransportationMethodstoWork_DEPARTURE_LONG',
                     'TransportationMethodstoWork_TRAVEL_LONG',
                     'TransportationMethodstoWork_VEHICLESAVAILABLE_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Transportation Methods to Work'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]



# -- Work Hours -- #
dummy_labels_list = ['Usual Hours Worked Weekly',
                     'Mean Hours Worked Weekly',
                     'Mean Hours Worked Weekly (Over Time)',
                    ]
dummy_values_list = ['WorkHours_USUALHOURS_LONG',
                     'WorkHours_MEANHOURS_LONG',
                     'WorkHours_MEANHOURS_TIME',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Work Hours'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]



# -- Economic Measures -- #
dummy_labels_list = ['Civilian Workers by Industry',
                     'Civilian Workers by Occupation',
                     'Civilian Workers by Sector',
                     'Median Earnings for All Workers by Industry',
                     'Median Earnings for Full-Time Workers by Industry',
                     'Gender Pay Gap, Full-Time Workers (Coming Soon!)',
                     'Gender Pay Gap, All Workers (Coming Soon!)'
                    ]
dummy_values_list = ['EconomicMeasures_INDUSTRY_LONG',
                     'EconomicMeasures_OCCUPATION_LONG',
                     'EconomicMeasures_CLASS_LONG',
                     'EconomicMeasures_INDUSTRYEARNINGS_LONG',
                     'EconomicMeasures_INDUSTRYFULLEARNINGS_LONG',
                     'EconomicMeasures_GENDERPAYGAPFULL_LONG',
                     'EconomicMeasures_GENDERPAYGAPALL_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Economic Measures'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]

disabled_values = ['EconomicMeasures_GENDERPAYGAPFULL_LONG', 'EconomicMeasures_GENDERPAYGAPALL_LONG']
submeasures_dict['Economic Measures']  = [dict(item, **{'disabled': True}) if item['value'] in disabled_values else dict(item) for item in submeasures_dict['Economic Measures'] ]


# -- Population -- #
dummy_labels_list = ['Population by Age',
                     'Population by Race',
                     'Hispanic/Latino Population',
                     'Asian Population',
                     'American Indian and Alaska Native Population',
                     'Native Hawaiian and Pacific Islander Population',
                    ]
dummy_values_list = ['Population_AGE_LONG',
                     'Population_RACE_LONG',
                     'Population_HISPANICLATINO_LONG',
                     'Population_ASIAN_LONG',
                     'Population_INDIGENOUS_LONG',
                     'Population_NATIVEHAWAIIANPACIFICISLANDER_LONG'
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Population'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]



# -- Education -- #
dummy_labels_list = ['Attainment by Citizenship',
                     'Attainment, White',
                     'Attainment, Black',
                     'Attainment, American Indian & Alaska Native',
                     'Attainment, Asian',
                     'Attainment, Native Hawaiian & Pacific Islander',
                     'Attainment, Some Other Race',
                     'Attainment, Two or More Races',
                     'Attainment, White (Not Hispanic/Latino)',
                     'Attainment, Hispanic/Latino',
                     'Attainment, 18 to 24',
                     'Attainment, 25 to 34',
                     'Attainment, 35 to 44',
                     'Attainment, 45 to 64',
                     'Attainment, 65 and Older',
                    ]
dummy_values_list = ['Education_CITIZENSHIP_LONG',
                     'Education_RACE_WHITE_LONG',
                     'Education_RACE_BLACK_LONG',
                     'Education_RACE_INDIGENOUS_LONG',
                     'Education_RACE_ASIAN_LONG',
                     'Education_RACE_NATIVEHAWAIIANPACIFICISLANDER_LONG',
                     'Education_RACE_SOMEOTHERRACE_LONG',
                     'Education_RACE_TWOORMORERACES_LONG',
                     'Education_RACE_WHITENOTHISPANIC_LONG',
                     'Education_RACE_HISPANIC_LONG',
                     'Education_AGE_18to24_LONG',
                     'Education_AGE_25to34_LONG',
                     'Education_AGE_35to44_LONG',
                     'Education_AGE_45to64_LONG',
                     'Education_AGE_65andOlder_LONG',
                    ]
dummy_tuple = zip(dummy_labels_list, dummy_values_list)
submeasures_dict['Education'] = [{'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j} for i, j in dummy_tuple]