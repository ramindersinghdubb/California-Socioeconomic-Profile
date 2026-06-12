window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside_off_canvas_callbacks = {
    /**
     * Display the off-canvas.
     * 
     * @param {Number} n_clicks 
     * @param {Boolean} is_open 
     * @returns The off-canvas state.
     */
    display_canvas_function: function (n_clicks, is_open) {
        var canvas_state = is_open;
        
        if ( n_clicks ) {
            var canvas_state = true;
        }
        
        return canvas_state;
    },
    
    /**
     * Display the help text for the selected measure in the off-canvas body.
     * 
     * @param {String} selected_measure The selected measure.
     * @returns {HTMLSpanElement}
     */
    display_canvas_help_function: function (selected_measure) {
        if ( selected_measure == 'ContractRent' ) {
            return `<span style='font-size:22px;'>Contract Rent</span></u><br>
            <span style='color:#85BCC7;'>Contract rents</span> are defined as "the monthly rent agreed to or contracted for, regardless
            of any furnishings, utilities, fees, meals, or services that may be included" (2024 American Community Survey Design & Methodology Report, Chapter 6).<br><br><br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'RentBurden' ) {
            return `<span style='font-size:22px;'>Rent Burden</span></u><br>
            Renters who are <span style='color:#DC143C;'>rent-burdened</span> pay <u style='color:#DC143C;'><span style='color:#DC143C;'>over 30%</span></u> of their household income to rent.<br><br>
            Renters who are <span style='color:#B22222;'>severely rent-burdened</span> pay <u style='color:#B22222;'><span style='color:#B22222;'>over 50%</span></u> of their household income to rent.<br><br>
            Rent burden and severe rent burden is found by taking the percentage of household income going to gross rent. <span style='color:#85BCC7;'>Gross rent</span> is defined as
            "[the monthly rent agreed to or contracted for, regardless of any furnishings, utilities, fees, meals, or services that may be included] plus the estimated average monthly cost of utilities and fuels,
            if these are paid by the renter" (2024 American Community Survey Design & Methodology Report, Chapter 6). <br><br><br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'EmploymentStatistics' ) {
            return `<span style='font-size:22px;'>Employment Statistics</span></u><br>
            The <span style='color:#85BCC7;'>unemployment rate</span> is defined as the proportion of persons in the labor force who did not work in the reference period under question but were actively searching for work
            during the reference period in question.<br><br>
            The <span style='color:#85BCC7;'>labor force participation rate</span> (or <span style='color:#85BCC7;'>LFPR</span>) is defined as the proportion of working-aged (16 and older) persons who are
            working or actively searching for work.<br><br>
            The <span style='color:#85BCC7;'>employment-to-population ratio</span> (or <span style='color:#85BCC7;'>EPOP</span>) is defined as the proportion of working-aged (16 and older) persons who are
            working.<br><br>
            Per the 2024 American Community Survey Design & Methodology Report, questions regarding labor force status are designed to identify the following: <br><br>
            1) people who worked at any time during the reference week; <br>
            2) people on temporary layoff who were available for work; <br>
            3) people who did not work during the reference week but who had jobs or businesses from which they were temporarily absent (excluding layoffs); <br>
            4) people who did not work but were available during the reference week, and who were looking for work during the last four weeks; and <br>
            5) people not in the labor force. <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'FoodStamps' ) {
            return `<span style='font-size:22px;'>Food Stamps</span></u><br>
            Per the 2024 American Community Survey Design & Methodology Report, "the Food and Nutrition Service of the U.S. Department of Agriculture (USDA) administers the <span style='color:#85BCC7;'>Supplemental Nutrition Assistance (Food Stamp) Program (SNAP)</span> through state and local welfare offices.
            This program is the major national income-support program for which all low-income and low-resource households, regardless of household characteristics, are eligible.
            This question asks if anyone in the households received SNAP benefits at any time during the 12-month period before the ACS interview."
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'HealthInsuranceCoverage' ) {
            return `<span style='font-size:22px;'>Health Insurance Coverage</span></u><br>
            Per the 2024 American Community Survey Design & Methodology Report, "[the insured and uninsured population is assessed] by asking about coverage through an employer, direct purchase from an insurance company, Medicare, Medicaid or
            other government-assistance health plans, military health care, Veterans Affairs health care, Indian Health Service, or other types of health insurance or coverage
            plans. Plans that cover only one type of health care (such as dental plans) or plans that only cover a person in case of an accident or disability are not included."
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'HouseholdIncome' ) {
            return `<span style='font-size:22px;'>Household Income</span></u><br>
            <span style='color:#85BCC7;'>Income</span> is defined as "the sum of the amounts reported separately for wage or salary income; net self-employment income; interest, dividends, or net rental or royalty income,
            or income from estates and trusts; social security or railroad retirement income; Supplemental Security Income; public assistance or welfare payments;
            retirement, survivor, or disability pensions; and all other income. Income is reported for the past 12 months from the date of the interview. The estimates
            are inflation-adjusted using the Consumer Price Index" (2024 American Community Survey Design & Methodology Report, Chapter 6). 
            <br><br>
            To adjust for changes in cost of living, adjustment to the 2023 Consumer Price Index ("constant dollars") was conducted for data years earlier than 2023 through the
            <u><a href='https://www.bls.gov/cpi/additional-resources/chained-cpi.htm'>Bureau of Labor Statistics Chained Consumer Price Index for All Urban Consumers (C-CPI-U)</a></u> series.
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            1) <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u><br>
            2) <u><a href='https://www.census.gov/topics/income-poverty/income/guidance/current-vs-constant-dollars.html'>Current versus Constant (or Real) Dollars</a></u>`;
        }
        
        if ( selected_measure == 'HousingUnitsandOccupancy' ) {
            return `<span style='font-size:22px;'>Housing and Occupancy</span></u><br>
            The reference person, or <span style='color:#85BCC7;'>householder</span>, is usually "the person, or one of the people,
            in whose name the home is owned, being bought, or rented and who is listed as 'Person 1' on the survey questionnaire.
            If there is no such person in the household, any adult household member 15 and older can be designated" (2024 American Community Survey Design &
            Methodology Report, Chapter 6).
            <br><br><br>
            A property's <span style='color:#85BCC7;'>value</span> is computed based on: <br>
            "the respondent’s estimate of how much the property (house and lot, mobile home and lot, or condominium unit) would sell for.
            The information is collected for [housing units] that are owned or being bought and for vacant [housing units] that are for sale.
            If the house or mobile home is owned or being bought, but the land on which it sits is not, the respondent is asked to estimate the
            combined value of the house or mobile home and the land. For vacant [housing units], value is defined as the price asked for the
            property. This information is obtained from real estate agents, property managers, or neighbors" (ibis.). 
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'Poverty' ) {
            return `<span style='font-size:22px;'>Poverty Estimates</span></u><br>
            <span style='color:#85BCC7;'>Poverty</span> is not a directly asked question in the American Community Survey but formulated indirectly
            with the assistance of information regarding respondents' income and household composition (2024 American Community Survey Design & Methodology Report, Chapter 10).<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
        
        if ( selected_measure == 'TransportationMethodstoWork' ) {
            return `<span style='font-size:22px;'>Work Commute Estimates</span></u><br>
            <span style='color:#85BCC7;'>Commute methods to work</span> refer to "the principal mode of travel or type of conveyance
            that the worker usually used to get from home to work during the reference week" (2024 American Community Survey Design & Methodology Report, Chapter 6).<br><br>
            <span style='color:#85BCC7;'>Departure times</span> refer to "the time of day that the respondent usually
            left home to go to work during the reference week" (ibis.).<br><br>
            <span style='color:#85BCC7;'>Travel times</span> to work refer to the number of minutes it usually takes the respondent to get from home to
            work during the reference week (ibis.).<br><br>
            <span style='color:#85BCC7;'>Vehicles available</span> show
            <br>
            "the number of passenger cars, vans, and pickup or panel trucks of one-ton capacity or less kept at home and available
            for the use of household members. Vehicles rented or leased for one month or more, company vehicles, and police and
            government vehicles are included if kept at home and used for nonbusiness purposes. Dismantled or immobile vehicles 
            are excluded, as are vehicles kept at home but used only for business purposes" (ibis.). 
            <br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'WorkHours' ) {
            return `<span style='font-size:22px;'>Working Hours</span></u><br>
            Estimates for <span style='color:#85BCC7;'>usual hours worked weekly</span> are reported for the civilian, 16 and older employed labor force.<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'CharacteristicsoftheEconomicPopulation' ) {
            return `<span style='font-size:22px;'>Other Economic Measures</span></u><br>
            Estimates are reported for the civilian, 16 and older employed labor force.<br><br>
            <span style='color:#85BCC7;'>Industry</span> refers to the particular sphere of trade a civilian worker is employed in.<br><br>
            <span style='color:#85BCC7;'>Occupation</span> relates to the services associated with a civilian worker's employment.<br><br>
            <span style='color:#85BCC7;'>Sector</span> refers to the relative jurisdiction under which a civilian worker's employment is conducted (i.e.
            'private-sector', 'public-sector', self-employed, and family work).<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'Population' ) {
            return `<span style='font-size:22px;'>Population Estimates</span></u><br>
            <span style='color:#85BCC7;'>Race</span> refers to the socio-political category that individuals report themselves as. Note that race
            is not rooted in science or biology. For instance, the fact that 'Black' (a color) and 'Asian' (a geographical point of
            reference) reflect popular contemporary understandings of race and racial taxonomies within the United States metropole are in no way
            symptomatic of any scientific consensus. Further, note too the vagueness of 'Asian': could it refer to individuals hailing from Iran just
            as much as others hailing from Laos, given their respective landmasses are located within the Asian continent, or does 'Asian' refer to a
            popular understanding of individuals from landmasses close to and/or bordering the eastern Pacific seaboard?<br><br>
            For these, and other reasons, population estimates segmented by race should instead be motivated by a socio-political-economic understanding
            of the ways in which certain peoples who have understood themselves distinctively as a community (or, loosely, "population") have come to be
            situated.<br><br>
            For purposes of demonstration, Punjab is taken as a point of reference. In what ways has im/migration policy affected the presence
            of members of the Punjabi community? How has economic precarity in Punjab affected Punjabi individuals situated along the metropole and their
            relationships with both Punjab and the metropole? In what ways have existing community groups and structures (e.g. <i>gurdwaras</i>) made
            certain places more favorable to Punjabi individuals and the making of the Punjabi community?<br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }

        if ( selected_measure == 'Education' ) {
            return `<span style='font-size:22px;'>Educational Attainment</span></u><br>
            <span style='color:#85BCC7;'>Educational attainment</span>, unless otherwise stated, is reported for the <span style='color:#85BCC7;'>25 year and older</span> population.<br><br><br>
            <span style='font-size:22px;'>Sources</span><br>
            <u><a href='https://www2.census.gov/programs-surveys/acs/methodology/design_and_methodology/2024/acs_design_methodology_report_2024.pdf'>2024 American Community Survey Design & Methodology Report</a></u>`;
        }
    }
}