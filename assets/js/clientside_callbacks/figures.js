// This will be cleaned up. Hopefully. (TODO)

window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside_figure_callbacks = {
    /**
     * 
     * Generate a Plotly choropleth map.
     * 
     * @param {Number} selected_year The selected calendar year.
     * @param {String} selected_place The selected city/place.
     * @param {String} selected_measure The selected measure.
     * @param {String} selected_submeasure The submeasure (if selected).
     * @param {Array} masterfile The masterfile data.
     * @param {Array} mapfile The center-point data.
     * @param {Map} color_dict A map with continuous color scales (used for the colorbar).
     * @returns {Map} A map whose key-value pairs are sanitized by Plotly to generate
     * a choropleth map.
     */
    choropleth_map_function: function(selected_year, selected_place, selected_measure, selected_submeasure, masterfile, mapfile, color_dict) {
        var my_array = masterfile.filter(item => item['YEAR'] === selected_year);

        var locations_array = my_array.map(({GEO_ID}) => GEO_ID);

        var customdata_array = my_array.map(({TRACT}) => TRACT);

        if (selected_measure == 'ContractRent') {
            var z_array = my_array.map(({ESTIMATE_Mediancontractrent}) => ESTIMATE_Mediancontractrent);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Contract Rent (" + item['YEAR'] + "): <b style='color:#A91B0D; font-size:14px;'>" + item['ESTIMATE_Mediancontractrent_string'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = 'YlOrRd';
            var colorbar_title_text = '<b>Median<br>Contract<br>Rents (USD)</b>';
            var colorbar_tickprefix = '$';
            var colorbar_ticksuffix = '';

            var zmin = 0;
            var zmax = 3500;

            if (selected_year <= 2014){
                var zmin = 0;
                var zmax = 2000;
            }
            
            var zauto_bool = false;
        }
        
        if (selected_measure == 'RentBurden') {
            var z_array = my_array.map(({ESTIMATE_Totalrenters_RentBurden}) => ESTIMATE_Totalrenters_RentBurden);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percentage of Rent-Burdened&nbsp;&nbsp;<br>Renters (" + item['YEAR'] + "): <b style='color:#610C04; font-size:14px;'>" + item['ESTIMATE_Totalrenters_RentBurden'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = 'YlOrRd';
            var colorbar_title_text = '<b>Percentage of<br>Rent-Burdened<br>Individuals</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'EmploymentStatistics') {
            if (selected_submeasure != undefined && selected_submeasure.includes("UNEMP")){
                var z_array = my_array.map(({ESTIMATE_UNEMP_16andOlder}) => ESTIMATE_UNEMP_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Unemployment Rate (" + item['YEAR'] + "): <b style='color:#800000; font-size:14px;'>" + item['ESTIMATE_UNEMP_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'YlOrRd';
                var colorbar_title_text = '<b>Unemp.<br>Rate</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin = 0;
                var zmax = 20;
                var zauto_bool = false;
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("LFPR")){
                var z_array = my_array.map(({ESTIMATE_LFPR_16andOlder}) => ESTIMATE_LFPR_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Labor Force Participation Rate (" + item['YEAR'] + "): <b style='color:#7A4988; font-size:14px;'>" + item['ESTIMATE_LFPR_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'Viridis';
                var colorbar_title_text = '<b>Labor<br>Force<br>Participat.<br>Rate</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin;
                var zmax;
                var zauto_bool = true;
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("EPOP")){
                var z_array = my_array.map(({ESTIMATE_EPOP_16andOlder}) => ESTIMATE_EPOP_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Employment-to-Population Ratio (" + item['YEAR'] + "): <b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_EPOP_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'Greens';
                var colorbar_title_text = '<b>Employment-<br>to-Population<br>Ratio</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin = 20;
                var zmax = 80;
                var zauto_bool = false;
            }
            if (selected_submeasure == undefined) {
                var z_array = my_array.map(({ESTIMATE_UNEMP_16andOlder}) => ESTIMATE_UNEMP_16andOlder);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Population: 16 and older</span>" + "<br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Unemployment Rate (" + item['YEAR'] + "): <b style='color:#800000; font-size:14px;'>" + item['ESTIMATE_UNEMP_16andOlder'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = 'YlOrRd';
                var colorbar_title_text = '<b>Unemp.<br>Rate</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '%';
                var zmin = 0;
                var zmax = 20;
                var zauto_bool = false;
            }
        }
        
        if (selected_measure == 'FoodStamps') {
            var z_array = my_array.map(({PERCENT_HouseholdsreceivingfoodstampsSNAP}) => PERCENT_HouseholdsreceivingfoodstampsSNAP);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percentage of Households Receiving&nbsp;&nbsp;<br>Food Stamps (" + item['YEAR'] + "): <b style='color:#559C9E; font-size:14px;'>" + item['PERCENT_HouseholdsreceivingfoodstampsSNAP'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['DarkMint'];
            var colorbar_title_text = '<b>Percentage of<br>Households<br>Receiving<br>Food Stamps</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'HouseholdIncome') {
            var z_array = my_array.map(({ESTIMATE_Households_Meanincomedollars}) => ESTIMATE_Households_Meanincomedollars);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Household Income (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>$" + item['ESTIMATE_Households_Meanincomedollars'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Emrld'];
            var colorbar_title_text = '<b>Median<br>Household<br>Income</b>';
            var colorbar_tickprefix = '$';
            var colorbar_ticksuffix = '';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'HousingUnitsandOccupancy') {
            var z_array = my_array.map(({ESTIMATE_TotalHousingUnits}) => ESTIMATE_TotalHousingUnits);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Housing Units (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_TotalHousingUnits'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            
            var colorscale_color = 'Greens';
            var colorbar_title_text = '<b>Total<br>Housing<br>Units</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';

            if (selected_submeasure != undefined && selected_submeasure.includes("_HOMEVALUE_")){
                var z_array = my_array.map(({ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars}) => ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Owner-Occupied Home Value (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_VALUE_Owneroccupiedhousingunits_Mediandollars_string'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['Emrld'];
                var colorbar_title_text = '<b>Median<br>Owner-<br>Occupied<br>Home<br>Value</b>';
                var colorbar_tickprefix = '$';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("SMOC")){
                var z_array = my_array.map(({ESTIMATE_SELECTEDMONTHLYOWNERCOSTSSMOC_Housingunitswithamortgage_Mediandollars}) => ESTIMATE_SELECTEDMONTHLYOWNERCOSTSSMOC_Housingunitswithamortgage_Mediandollars);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Median Monthly Owner Costs (" + item['YEAR'] + "): <br><b style='color:#234F1E; font-size:14px;'>" + item['ESTIMATE_SELECTEDMONTHLYOWNERCOSTSSMOC_Housingunitswithamortgage_Mediandollars'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                
                var colorscale_color = color_dict['Hot'];
                var colorbar_title_text = '<b>Median<br>Monthly<br>Owner<br>Costs</b>';
                var colorbar_tickprefix = '$';
                var colorbar_ticksuffix = '';
            }
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }
        
        if (selected_measure == 'Poverty') {
            var z_array = my_array.map(({ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined}) => ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percent Below Poverty Level (" + item['YEAR'] + "): <br><b style='color:#420C09; font-size:14px;'>" + item['ESTIMATE_Percentbelowpovertylevel_Populationforwhompovertystatusisdetermined'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Magma'];
            var colorbar_title_text = '<b>Percent<br>Below<br>Poverty<br>Level</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'HealthInsuranceCoverage') {
            var z_array = my_array.map(({PERCENT_Uninsured_Civiliannoninstitutionalizedpopulation}) => PERCENT_Uninsured_Civiliannoninstitutionalizedpopulation);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Percentage Uninsured  (" + item['YEAR'] + "): <b style='color:#710C04; font-size:14px;'>" + item['PERCENT_Uninsured_Civiliannoninstitutionalizedpopulation'] + "%</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Hot'];
            var colorbar_title_text = '<b>Percentage<br>Uninsured</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '%';
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'TransportationMethodstoWork') {
            var z_array = my_array.map(({PERCENT_Total_Workers16yearsandoverwhodidnotworkfromhome_TRAVELTIMETOWORK_Meantraveltimetoworkminutes}) => PERCENT_Total_Workers16yearsandoverwhodidnotworkfromhome_TRAVELTIMETOWORK_Meantraveltimetoworkminutes);
            var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Average Work Commute Time (" + item['YEAR'] + "): <br><b style='color:#B2560D; font-size:14px;'>" + item['PERCENT_Total_Workers16yearsandoverwhodidnotworkfromhome_TRAVELTIMETOWORK_Meantraveltimetoworkminutes'] + " minutes </b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
            var colorscale_color = color_dict['OrRd'];
            var colorbar_title_text = '<b>Average<br>Travel<br>Time<br>(Mins.)</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '<br>mins.';
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'WorkHours') {
            var z_array = my_array.map(({ESTIMATE_Total_Population16to64years_Meanusualhoursworkedforworkers}) => ESTIMATE_Total_Population16to64years_Meanusualhoursworkedforworkers);
            var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Average Usual Hours Worked (" + item['YEAR'] + "): <br><b style='color:#070504; font-size:14px;'>" + item['ESTIMATE_Total_Population16to64years_Meanusualhoursworkedforworkers'] + " hours </b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
            var colorscale_color = color_dict['OrRd'];
            var colorbar_title_text = '<b>Average<br>Usual<br>Hours<br>Worked<br></b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '<br>hrs.';
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'EconomicMeasures') {
            var z_array = my_array.map(({ESTIMATE_EMPLOYMENTSTATUS_Population16yearsandover_Inlaborforce_Civilianlaborforce}) => ESTIMATE_EMPLOYMENTSTATUS_Population16yearsandover_Inlaborforce_Civilianlaborforce);
            var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Number of Civilian Employed Workers (" + item['YEAR'] + "): <br><b style='color:#070504; font-size:14px;'>" + item['ESTIMATE_EMPLOYMENTSTATUS_Population16yearsandover_Inlaborforce_Civilianlaborforce'] + " </b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
            var colorscale_color = color_dict['Emrld'];
            var colorbar_title_text = '<b>Civilian<br>Employed<br>Workers</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'Population') {
            var z_array = my_array.map(({ESTIMATE_SEXANDAGE_Totalpopulation}) => ESTIMATE_SEXANDAGE_Totalpopulation);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_SEXANDAGE_Totalpopulation'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            
            var colorscale_color = color_dict['deep'];
            var colorbar_title_text = '<b>Total<br>Population</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';

            if (selected_submeasure != undefined && selected_submeasure.includes("_HISPANICLATINO_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_HispanicorLatinoofanyrace}) => ESTIMATE_RACE_Totalpopulation_HispanicorLatinoofanyrace);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Hispanic/Latino Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_HispanicorLatinoofanyrace'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total<br>Hispanic<br>and Latino<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("_ASIAN_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_Onerace_Asian}) => ESTIMATE_RACE_Totalpopulation_Onerace_Asian);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Asian Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_Onerace_Asian'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total<br>Asian<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("_INDIGENOUS_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_Onerace_AmericanIndianandAlaskaNative}) => ESTIMATE_RACE_Totalpopulation_Onerace_AmericanIndianandAlaskaNative);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total American Indian and Alaska Native Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_Onerace_AmericanIndianandAlaskaNative'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total<br>American<br>Indian and<br>Alaska<br>Native<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }

            if (selected_submeasure != undefined && selected_submeasure.includes("_NATIVEHAWAIIANPACIFICISLANDER_")){
                var z_array = my_array.map(({ESTIMATE_RACE_Totalpopulation_Onerace_NativeHawaiianandOtherPacificIslander}) => ESTIMATE_RACE_Totalpopulation_Onerace_NativeHawaiianandOtherPacificIslander);
                var strings = my_array.map(function(item) {
                    return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                    + "<span style='font-family: Trebuchet MS, sans-serif;'>Total Native Hawaiian and Pacific Islander Population (" + item['YEAR'] + "): <br><b style='color:rgb(62, 108, 150); font-size:14px;'>" + item['ESTIMATE_RACE_Totalpopulation_Onerace_NativeHawaiianandOtherPacificIslander'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
                });
                var colorscale_color = color_dict['deep'];
                var colorbar_title_text = '<b>Total Native<br>Hawaiian<br>and Pacific<br>Islander<br>Population</b>';
                var colorbar_tickprefix = '';
                var colorbar_ticksuffix = '';
            }
            
            var zmin;
            var zmax;
            var zauto_bool = true;
        }

        if (selected_measure == 'Education') {
            var z_array = my_array.map(({ESTIMATE_TOTAL_CITIZENSHIPSTATUS}) => ESTIMATE_TOTAL_CITIZENSHIPSTATUS);
            var strings = my_array.map(function(item) {
                return "<b style='font-size:16px;'>" + item['TRACT'] + "</b><br>" + "<span style='font-family: Trebuchet MS, sans-serif;'>" + item['CITY'] + ", " + item['COUNTY'] + "</span>" + "<br><br>"
                + "<span style='font-family: Trebuchet MS, sans-serif;'>Total 25 and Older Population (" + item['YEAR'] + "): <br><b style='color:#070504; font-size:14px;'>" + item['ESTIMATE_TOTAL_CITIZENSHIPSTATUS'] + "</b></span> &nbsp;&nbsp;&nbsp;&nbsp;<br><br><extra></extra>";
            });
            var colorscale_color = color_dict['Emrld'];
            var colorbar_title_text = '<b>25 and<br>Older<br>Population</b>';
            var colorbar_tickprefix = '';
            var colorbar_ticksuffix = '';
            var zmin;
            var zmax;
            var zauto_bool = true;

            if (selected_submeasure != undefined && selected_submeasure.includes("_AGE_")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_AGE}) => ESTIMATE_TOTAL_AGE);
                var colorbar_title_text = '<b>18 and<br>Older<br>Population</b>';
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("_WHITE_")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_White}) => ESTIMATE_TOTAL_RACE_White);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("BLACK")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_BlackorAfricanAmerican}) => ESTIMATE_TOTAL_RACE_BlackorAfricanAmerican);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("INDIGENOUS")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_AmericanIndianandAlaskaNative}) => ESTIMATE_TOTAL_RACE_AmericanIndianandAlaskaNative);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("ASIAN")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_Asian}) => ESTIMATE_TOTAL_RACE_Asian);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("NATIVEHAWAIIANPACIFICISLANDER")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_NativeHawaiianandOtherPacificIslander}) => ESTIMATE_TOTAL_RACE_NativeHawaiianandOtherPacificIslander);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("SOMEOTHERRACE")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_Someotherrace}) => ESTIMATE_TOTAL_RACE_Someotherrace);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("TWOORMORERACES")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_Twoormoreraces}) => ESTIMATE_TOTAL_RACE_Twoormoreraces);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("WHITENOTHISPANIC")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_WhitenotHispanicorLatino}) => ESTIMATE_TOTAL_RACE_WhitenotHispanicorLatino);
            }
            if (selected_submeasure != undefined && selected_submeasure.includes("_HISPANIC_")){
                var z_array = my_array.map(({ESTIMATE_TOTAL_RACE_HispanicorLatinoofanyrace}) => ESTIMATE_TOTAL_RACE_HispanicorLatinoofanyrace);
            }
            
        }


        
        

        var geometry_url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_CensusTract_Mapfiles/${selected_year}/mastergeometry_${selected_place}_${selected_year}.geojson`;

        
        var main_data = {
            'type': 'choroplethmap',
            'customdata': customdata_array,
            'geojson': geometry_url,
            'locations': locations_array,
            'featureidkey': 'properties.GEO_ID',
            'colorscale': colorscale_color,
            'reversescale': true,
            'z': z_array,
            'zmin': zmin, 'zmax': zmax, 'zauto': zauto_bool,
            'marker': {'line': {'color': '#020403', 'width': 1.75}, 'opacity': 0.6},
            'text': strings,
            'colorbar': {'outlinewidth': 2,
                        'ticklabelposition': 'outside bottom',
                        'tickprefix': colorbar_tickprefix,
                        'ticksuffix': colorbar_ticksuffix,
                        'title': {'font': {'color': '#020403', 'weight': 500}, 'text': colorbar_title_text},
                        'tickfont': {'weight': 500}},
            'hoverlabel': {'bgcolor': '#FAFAFA', 'bordercolor': '#BEBEBE', 'font': {'color': '#020403'}},
            'hovertemplate': '%{text}'
        };

        var map_array = mapfile.filter(item => item['PLACE'] === selected_place);

        var long_array = map_array.map(({LON}) => LON);
        var long_center = long_array.reduce((a, b) => a + b) / long_array.length;
        const lon_center = parseFloat(long_center.toFixed(7));
        
        var lat_array = map_array.map(({LAT}) => LAT);
        var lati_center = lat_array.reduce((a, b) => a + b) / lat_array.length;
        const lat_center = parseFloat(lati_center.toFixed(7));

        var layout = {
            'autosize': true,
            'height': window.screen.height,
            'hoverlabel': {'align': 'left'},
            'map': {'center': {'lat': lat_center, 'lon': lon_center}, 'style': 'streets', 'zoom': 11},
            'margin': {'b': 0, 'l': 0, 'r': 0, 't': 0},
            'paper_bgcolor': '#FEF9F3',
            'plot_bgcolor': '#FEF9F3',
        };

        

        if (selected_submeasure !== undefined && selected_submeasure !== null) {
            main_data['hoverinfo'] = 'none';
            main_data['hovertemplate'] = null;
        }
        if (selected_submeasure === null) {
            main_data['hoverinfo'] = 'all';
            main_data['hovertemplate'] = '%{text}';
        }

        return {'data': [main_data], 'layout': layout};

    },

    /**
     * 
     * Generate the tooltip figure. The figure is either a scatter-line plot, or
     * a bar graph.
     * 
     * @param {Number} selected_year The selected calendar year.
     * @param {String} selected_submeasure The submeasure (if selected).
     * @param {Array} hoverData The bound box data for the hovered census tract.
     * @param {Array} tooltip_data The tooltip data.
     * @param {Map} discrete_color_dict A map with discrete color scales.
     * @param {String} selected_place The selected place.
     * @returns {Map} A map whose key-value pairs are sanitized by Plotly to generate a
     * Plotly-Express figure.
     */
    tooltip_figure_function: function(selected_year, selected_submeasure, hoverData, tooltip_data, discrete_color_dict, selected_place) {
        if (!hoverData) {
            return [false, window.dash_clientside.no_update, window.dash_clientside.no_update];
        }

        if (!selected_submeasure) {
            return [false, window.dash_clientside.no_update, window.dash_clientside.no_update];
        } else {
            var tract_name = hoverData['points']['0']['customdata'];
            
            var city_string = selected_place;

            var barmode;
            
            if ( selected_submeasure.includes("LONG") ) {
                var my_array = tooltip_data.filter(item => item['YEAR'] == selected_year && item['TRACT'] == tract_name);
                
                var x_array = my_array.map(({variable}) => variable);
                var xaxis_standoff = 10;
                

                if ( selected_submeasure.startsWith("ContractRent") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                    });
                    
                    if (selected_year < 2015){
                        var color_array = discrete_color_dict['YlOrRd_9'];
                    } else {
                        var color_array = discrete_color_dict['YlOrRd_12'];
                    }
                    var xaxis_title_text = '<b>Contract Rent</b>';
                    
                    var yaxis_title_text = '<b>Number of Units</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                    var xlabels_size = 9;
                    
                    var title_text = `<b>Distribution of Contract Rents, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("RentBurden") && !selected_submeasure.includes("AGE") && !selected_submeasure.includes("INCOME") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Reds_2'];

                    var xaxis_title_text = '<b>Rent Burden Categories</b>';
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Percentage of Renters by Rent Burden Severity, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("AGE_LONG") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Same_Reds_5'];

                    var xaxis_title_text = '<b>Age Groups</b>';
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Percentage of Rent-Burdened Renters by Age, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("INCOME_LONG") ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Same_Reds_8'];

                    var xaxis_title_text = '<b>Income Categories</b>';
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Percentage of Rent-Burdened Renters by Income, ${selected_year}</b>`;

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("RACE_LONG")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['G10'];

                    var xaxis_title_text = '<b>Racial Categories</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 9;
                    var x_tickvals = ['Overall (16 and Older)', 'White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin (of any race)', 'White, not Hispanic or Latino'];
                    var x_ticktext = ['Overall (16 and<br>Older)', 'White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Race, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Race, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Race, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }
                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("SEX_LONG")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['D3_7'];

                    var xaxis_title_text = '<b>Sex and Women with Children</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 9;
                    var x_tickvals = ['Overall (20 to 64)', 'Male', 'Female', 'Female (With children under 6 years old)', 'Female (With children under 18 years old)', 'Female (With children under 17 years old)', 'Female (With children 6 to 17 years old)'];
                    var x_ticktext = ['Overall (20 to 64)', 'Male', 'Female', 'Female (With children<br>under 6 years old)', 'Female (With children<br>under18 years old)', 'Female (With children<br>under 17 years old)', 'Female (With children<br>6 to 17 years old)'];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Sex, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Sex, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Sex, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }
                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("EDUCATIONALSTATUS_LONG")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['D3_5'];

                    var xaxis_title_text = '<b>Educational Attainment </b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 10;
                    var x_tickvals = ['Overall (25 to 64)', 'Less than high school graduate', 'High school graduate (includes equivalency)', "Some college or associate's degree", "Bachelor's degree or higher"];
                    var x_ticktext = ['Overall (25 to 64)', 'Less than high<br>school graduate', 'High school graduate<br>(or equivalent)', "Some college or<br>associate's degree", "Bachelor's degree<br>or higher"];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Educational Attainment, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Educational Attainment, ${selected_year}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Educational Attainment, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }
                if ( selected_submeasure.startsWith("FoodStamps")  ) {
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_YES}) => value_YES);
                    var y2_array = my_array.map(({value_NO}) => value_NO);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';

                    var yaxis_title_text = '<b>Percentage of Households</b>';

                    if ( selected_submeasure.includes("RACE") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "%</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin (of any race)', 'White, not Hispanic or Latino'];
                        var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Race, ${selected_year}</b>`;
                    }
                    if ( selected_submeasure.includes("POVERTY") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Poverty Status</b>';
                        var xaxis_standoff = 15;
                        
                        var x_tickvals = ['Below poverty level', 'At or above poverty level'];
                        var x_ticktext = ['Below poverty level', 'At or above poverty level'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Poverty Status, ${selected_year}</b>`;
                    }
                    if ( selected_submeasure.includes("DISABILITYSTATUS") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Disability Status</b>';
                        var xaxis_standoff = 15;
                        
                        var x_tickvals = ['With one or more people with a disability', 'With no people with a disability',];
                        var x_ticktext = ['With one or more<br>people with a disability', 'With no people<br>with a disability'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Disability Status, ${selected_year}</b>`;
                    }
                    if ( selected_submeasure.includes("WORKINGSTATUS") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                        });
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Working Status</b>';
                        var xaxis_standoff = 15;
                        
                        var x_tickvals = ['No workers in past 12 months', '1 worker in past 12 months', '2 or more workers in past 12 months'];
                        var x_ticktext = ['No workers in<br>the past 12 months', 'One worker in the<br>past 12 months', 'Two or more workers<br>in the past 12 months'];
                        var title_text = `<b>Food Stamps Recipients/Non-Recipients by Working Status, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'Recipients',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(179,226,205)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Non-Recipients',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(253,205,172)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2];
                    
                }

                if ( selected_submeasure.startsWith("HouseholdIncome")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size = 9;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "%</b>";
                    });
                    var color_array = discrete_color_dict['Greens_10'];

                    var xaxis_title_text = '<b>Income</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    var xlabels_size = 10;
                    var x_tickvals = ['Less than $10,000', '$10,000 to $14,999', '$15,000 to $24,999', '$25,000 to $34,999', '$35,000 to $49,999', '$50,000 to $74,999', '$75,000 to $99,999', '$100,000 to $149,999', '$150,000 to $199,999', '$200,000 or more'];
                    var x_ticktext = ['Less than $10k', '$10k to 14.9k', '$15k to 24.9k', '$25k to 34.9k', '$35k to 49.9k', '$50k to 74.9k', '$75k to 99.9k', '$100k to 149.9k', '$150k to 199.9k', '$200k or more'];

                    if (selected_submeasure.includes("HOUSEHOLDS_LONG")){
                        var yaxis_title_text = '<b>Percent of Households</b>';
                        var title_text = `<b>Income Distribution for Households, ${selected_year}</b>`;
                    }
                    if (selected_submeasure.includes("FAMILIES_LONG")){
                        var yaxis_title_text = '<b>Percent of Families</b>';
                        var title_text = `<b>Income Distribution for Families, ${selected_year}</b>`;
                    }
                    if (selected_submeasure.includes("MARRIEDCOUPLEFAMILIES_LONG")){
                        var yaxis_title_text = '<b>Percent of Married-Couple<br>Families</b>';
                        var title_text = `<b>Income Distribution for Married-Couple Families, ${selected_year}</b>`;
                    }
                    if (selected_submeasure.includes("NONFAMILYHOUSEHOLDS_LONG")){
                        var yaxis_title_text = '<b>Percent of Nonfamily Households</b>';
                        var title_text = `<b>Income Distribution for Nonfamily Households, ${selected_year}</b>`;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("HousingUnitsandOccupancy")  ) {
                    if (selected_submeasure.includes("HOMEVALUE_LONG")){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Greens_10'];
    
                        var xaxis_title_text = '<b>Home Values</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 10;
                        
                        var x_tickvals = ['Less than $50,000', '$50,000 to $99,999', '$100,000 to $149,999', '$150,000 to $199,999', '$200,000 to $299,999', '$300,000 to $499,999', '$500,000 to $999,999', '$1,000,000 or more'];
                        var x_ticktext = ['Less than $50k', '$50k to 99.9k', '$100k to<br>149.9k', '$150k to<br>199.9k', '$200k to<br>299.9k', '$300k to<br>499.9k', '$500k to<br>999.9k', '$1 million<br>or more'];
                        
                        var yaxis_title_text = '<b>Number of Households</b>';
                        var title_text = `<b>Home Values for Owner-Occupied Housing Units, ${selected_year}</b>`;
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if (selected_submeasure.includes("_HOUSINGUNITS_")){
                        var barmode = 'group';
                        var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                        var y2_array = my_array.map(({value_OWNER}) => value_OWNER);
                        var y3_array = my_array.map(({value_RENTER}) => value_RENTER);
                        
                        var xlabels_size;
                        var x_ticktext;
                        var x_tickvals;
                        
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
    
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
    
                        if ( selected_submeasure.includes("RACE") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y3_text = y3_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            
                            var xlabels_size = 9;
                            var xaxis_title_text = '<b>Racial Categories</b>';
                            
                            var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin', 'White alone, not Hispanic or Latino'];
                            var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];
                            var title_text = `<b>Occupied Housing Units by Householder Race, ${selected_year}</b>`;
                        }
    
                        if ( selected_submeasure.includes("AGE") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            var y3_text = y3_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                            });
                            
                            var xlabels_size = 10;
                            var xaxis_title_text = '<b>Age</b>';
    
                            var x_tickvals = ['Under 35 years', '35 to 44 years', '45 to 54 years', '55 to 64 years', '65 to 74 years', '75 to 84 years', '85 years and over'];
                            var x_ticktext = ['Under 35<br>years', '35 to 44', '45 to 54', '55 to 64', '65 to 74', '75 to 84', '85 years and<br>Older'];
                            var title_text = `<b>Occupied Housing Units by Householder Age, ${selected_year}</b>`;
                        }
    
                        data1 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y1_array,
                            name: 'Total Occupied<br>Housing Units',
                            'text': y1_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': 'rgb(179,226,205)'
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
                        
                        data2 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y2_array,
                            name: 'Owner-Occupied<br>Units',
                            'text': y2_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': 'rgb(253,205,172)'
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        data3 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y3_array,
                            name: 'Renter-Occupied<br>Units',
                            'text': y3_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': 'rgb(203,213,232)'
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        var data = [data1, data2, data3];

                    }

                    if ( selected_submeasure.includes("YEARBUILT") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Oranges'];
    
                        var xaxis_title_text = '<b>Year Housing Unit Built</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 10;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Year Built, ${selected_year}</b>`;
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("UNITROOMS") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['GnBu'];
    
                        var xaxis_title_text = '<b>Rooms in Housing Unit</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Number of Rooms, ${selected_year}</b>`;

                        var x_tickvals = ['1 room', '2 rooms', '3 rooms', '4 rooms', '5 rooms', '6 rooms', '7 rooms', '8 rooms', '9 rooms or more'];
                        var x_ticktext = ['1 room', '2 rooms', '3 rooms', '4 rooms', '5 rooms', '6 rooms', '7 rooms', '8 rooms', '9 rooms<br>or more'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("UNITBEDROOMS") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['GnBu'];
    
                        var xaxis_title_text = '<b>Bedrooms in Housing Unit</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 11;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Number of Bedrooms, ${selected_year}</b>`;
                        var x_tickvals = ['No bedroom', '1 bedroom', '2 bedrooms', '3 bedrooms', '4 bedrooms', '5 or more bedrooms'];
                        var x_ticktext = ['No bedrooms', '1 bedroom', '2 bedrooms', '3 bedrooms', '4 bedrooms', '5 or more<br>bedrooms'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("HEATINGFUEL") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Pastel2'];
    
                        var xaxis_title_text = '<b>House Heating Fuel</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 10;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by House Heating Fuel, ${selected_year}</b>`;
                        var x_tickvals = ['Utility gas', 'Bottled, tank, or LP gas', 'Electricity', 'Fuel oil, kerosene, etc.', 'Coal or coke', 'Wood', 'Solar energy', 'Other fuel', 'No fuel used'];
                        var x_ticktext = ['Utility gas', 'Bottled, tank,<br>or LP gas', 'Electricity', 'Fuel oil, kerosene,<br>etc.', 'Coal or coke', 'Wood', 'Solar energy', 'Other fuel', 'No fuel used'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("LACKINGFACILITIES") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Pastel2'];
    
                        var xaxis_title_text = '<b>Type of Facilities</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        var xaxis_standoff = 20;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Lacking Facilities, ${selected_year}</b>`;
                        var x_tickvals = ['Lacking complete plumbing facilities', 'Lacking complete kitchen facilities', 'No telephone service available'];
                        var x_ticktext = ['Lacking complete<br>plumbing facilities', 'Lacking complete<br>kitchen facilities', 'No telephone service<br>available'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("OCCUPANTSPERROOM") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['Pastel2'];
    
                        var xaxis_title_text = '<b>Occupants Per Room</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units by Occupants Per Room, ${selected_year}</b>`;
                        var xaxis_standoff = 20;
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("MORTGAGESMOC") ){
                        var y_array = my_array.map(({value}) => value);
                        
                        var text = y_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                        });
                        var color_array = discrete_color_dict['YlOrRd_9'];
    
                        var xaxis_title_text = '<b>Monthly Owner Costs</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var xlabels_size = 12;
                        var xaxis_standoff = 20;
                        
                        var yaxis_title_text = '<b>Number of Housing Units</b>';
                        var title_text = `<b>Housing Units (with Mortgages) by Monthly Owner Costs, ${selected_year}</b>`;
                        var x_tickvals = ['Less than $500', '$500 to $999', '$1,000 to $1,499', '$1,500 to $1,999', '$2,000 to $2,499', '$2,500 to $2,999', '$3,000 or more', '$2,000 or more'];
                        var x_ticktext = ['Less than<br>$500', '$500 to<br>999', '$1,000 to<br>1,499', '$1,500 to<br>1,999', '$2,000 to<br>2,499', '$2,500 to<br>2,999', '$3,000 or<br>more', '$2,000 or<br>more'];
    
                        var data = [{
                            'type': 'bar',
                            'x': x_array,
                            'y': y_array,
                            'text': text,
                            'textposition': 'auto',
                            'marker': {'color': color_array,
                                    'line': {'color': '#111111', 'width': 1.5}
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        }];
                    }

                    if ( selected_submeasure.includes("YEARMOVEDIN") ){
                        if ( selected_year < 2017 ) {
                            var y_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                            
                            var text = y_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                            });
                            var color_array = discrete_color_dict['GnBu'];
        
                            var xaxis_title_text = '<b>Year Householder Moved In</b>';
                            var yaxis_tickprefix = '';
                            var yaxis_ticksuffix = '';
                            var xlabels_size = 12;
                            var xaxis_standoff = 20;
                            
                            var yaxis_title_text = '<b>Number of Housing Units</b>';
                            var title_text = `<b>Housing Units by Year Householder Built In, ${selected_year}</b>`;
                            var x_tickvals = ['1969 or earlier', '1970 to 1979', '1980 to 1989', '1990 to 1999', '2000 to 2004', '2005 or later', '2000 to 2009', '2010 or later', '1979 or earlier', '2010 to 2014', '2015 or later', '1989 or earlier', '2015 to 2016', '2017 or later', '2015 to 2018', '2019 or later', '2010 to 2017', '2018 to 2020', '2021 or later'];
                            var x_ticktext = ['1969 or<br>earlier', '1970 to<br>1979', '1980 to<br>1989', '1990 to<br>1999', '2000 to<br>2004', '2005 or<br>later', '2000 to<br>2009', '2010 or<br>later', '1979 or<br>earlier', '2010 to<br>2014', '2015 or<br>later', '1989 or<br>earlier', '2015 to<br>2016', '2017 or<br>later', '2015 to<br>2018', '2019 or<br>later', '2010 to<br>2017', '2018 to<br>2020', '2021 or<br>later'];
        
                            var data = [{
                                'type': 'bar',
                                'x': x_array,
                                'y': y_array,
                                'text': text,
                                'textposition': 'auto',
                                'marker': {'color': color_array,
                                        'line': {'color': '#111111', 'width': 1.5}
                                        },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            }];
                        }
                        if ( selected_year >= 2017 ) {
                            var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                            var y2_array = my_array.map(({value_OWNER}) => value_OWNER);
                            var y3_array = my_array.map(({value_RENTER}) => value_RENTER);
                            
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var y3_text = y3_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
        
                            var xaxis_title_text = '<b>Year Householder Moved In</b>';
                            var yaxis_tickprefix = '';
                            var yaxis_ticksuffix = '';
                            var xlabels_size = 12;
                            var xaxis_standoff = 20;
                            
                            var yaxis_title_text = '<b>Number of Housing Units</b>';
                            var title_text = `<b>Housing Units by Year Householder Built In, ${selected_year}</b>`;
                            var x_tickvals = ['1969 or earlier', '1970 to 1979', '1980 to 1989', '1990 to 1999', '2000 to 2004', '2005 or later', '2000 to 2009', '2010 or later', '1979 or earlier', '2010 to 2014', '2015 or later', '1989 or earlier', '2015 to 2016', '2017 or later', '2015 to 2018', '2019 or later', '2010 to 2017', '2018 to 2020', '2021 or later'];
                            var x_ticktext = ['1969 or<br>earlier', '1970 to<br>1979', '1980 to<br>1989', '1990 to<br>1999', '2000 to<br>2004', '2005 or<br>later', '2000 to<br>2009', '2010 or<br>later', '1979 or<br>earlier', '2010 to<br>2014', '2015 or<br>later', '1989 or<br>earlier', '2015 to<br>2016', '2017 or<br>later', '2015 to<br>2018', '2019 or<br>later', '2010 to<br>2017', '2018 to<br>2020', '2021 or<br>later'];

                            data1 = {
                                'type': 'bar',
                                'x': x_array,
                                'y': y1_array,
                                name: 'Total Housing<br>Units',
                                'text': y1_text,
                                'textposition': 'auto',
                                'marker': {'line': {'color': '#111111', 'width': 1.5},
                                        'color': 'rgb(179,226,205)'
                                        },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            };
                        
                            data2 = {
                                'type': 'bar',
                                'x': x_array,
                                'y': y2_array,
                                name: 'Owner-Occupied<br>Units',
                                'text': y2_text,
                                'textposition': 'auto',
                                'marker': {'line': {'color': '#111111', 'width': 1.5},
                                        'color': 'rgb(253,205,172)'
                                        },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            };
        
                            data3 = {
                                'type': 'bar',
                                'x': x_array,
                                'y': y3_array,
                                name: 'Renter-Occupied<br>Units',
                                'text': y3_text,
                                'textposition': 'auto',
                                'marker': {'line': {'color': '#111111', 'width': 1.5},
                                        'color': 'rgb(203,213,232)'
                                        },
                                'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                                'hoverinfo': 'none',
                                'hovertemplate': null
                            };
        
                            var data = [data1, data2, data3];
                        }
                    }
                    
                }

                if ( selected_submeasure.startsWith("Poverty") ) {
                    
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_BELOW}) => value_BELOW);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    var yaxis_title_text = '<b>Number of Individuals</b>';

                    if ( selected_submeasure.includes("RACE") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino origin (of any race)', 'White, not Hispanic or Latino'];
                        var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White, not Hispanic<br>or Latino'];
                        var title_text = `<b>Population Below Poverty Level by Race, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'Total Population',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(179,226,205)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Population Below<br>Poverty Level',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(251,180,174)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2];
                    
                }


                if ( selected_submeasure.startsWith("HealthInsuranceCoverage") ) {
                    
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_INSURED}) => value_INSURED);
                    var y3_array = my_array.map(({value_UNINSURED}) => value_UNINSURED);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    var yaxis_title_text = '<b>Number of Individuals</b>';

                    if ( selected_submeasure.includes("RACE") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'White, not Hispanic or Latino', 'Hispanic or Latino (of any race)'];
                        var x_ticktext = ['White', 'Black or African<br>American', 'American Indian and<br>Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'White, not Hispanic<br>or Latino', 'Hispanic or Latino<br>(of any race)'];
                        var title_text = `<b>Insurance Coverage by Race, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'Total Population',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(179,226,205)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Insured',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(253,205,172)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    data3 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y3_array,
                        name: 'Uninsured',
                        'text': y3_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(203,213,232)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3];
                    
                }



                if ( selected_submeasure.startsWith("TransportationMethodstoWork") ) {
                    
                    var barmode = 'group';
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_MALE}) => value_MALE);
                    var y3_array = my_array.map(({value_FEMALE}) => value_FEMALE);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    var yaxis_title_text = '<b>Number of Workers</b>';

                    if ( selected_submeasure.includes("_METHODSTOWORK_") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 10;
                        var xaxis_title_text = '<b>Methods of Transportation</b>';
                        
                        var x_tickvals = ['Drove alone', 'Carpooled', 'Public transportation (excluding taxicab)', 'Walked', 'Bicycle', 'Taxicab, motorcycle, or other means', 'Worked from home'];
                        var x_ticktext = ['Drove alone', 'Carpooled', 'Public transport<br>(excluding taxicab)', 'Walked', 'Bicycle', 'Taxicab, motorcycle,<br>or other means', 'Worked from<br>home'];
                        var title_text = `<b>Methods of Transportation for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    if ( selected_submeasure.includes("_DEPARTURE_") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var xaxis_title_text = '<b>Departure Times</b>';
                        
                        var x_tickvals = ['12:00AM to 4:59AM', '5:00AM to 5:29AM', '5:30AM to 5:59AM', '6:00AM to 6:29AM', '6:30AM to 6:59AM', '7:00AM to 7:29AM', '7:30AM to 7:59AM', '8:00AM to 8:29AM', '8:30AM to 8:59AM', '9:00AM to 11:59PM'];
                        var x_ticktext = ['12:00AM<br>to<br>4:59AM', '5:00AM<br>to<br>5:29AM', '5:30AM<br>to<br>5:59AM', '6:00AM<br>to<br>6:29AM', '6:30AM<br>to<br>6:59AM', '7:00AM<br>to<br>7:29AM', '7:30AM<br>to<br>7:59AM', '8:00AM<br>to<br>8:29AM', '8:30AM<br>to<br>8:59AM', '9:00AM<br>to<br>11:59PM'];
                        var title_text = `<b>Departure Times for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    if ( selected_submeasure.includes("_VEHICLESAVAILABLE_") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 12;
                        var xaxis_title_text = '<b>Vehicles Availability</b>';
                        
                        var x_tickvals = ['No vehicle available', '1 vehicle available', '2 vehicles available', '3 or more vehicles available'];
                        var x_ticktext = ['No vehicle', '1 vehicle', '2 vehicles', '3 or more<br>vehicles'];
                        var title_text = `<b>Vehicles Available for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    if ( selected_submeasure.includes("TRAVEL") ) {
                        var y1_text = y1_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:7px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 8;
                        var xaxis_title_text = '<b>Travel Times</b>';

                        var x_tickvals = ['Less than 10 minutes', '10 to 14 minutes', '15 to 19 minutes', '20 to 24 minutes', '25 to 29 minutes', '30 to 34 minutes', '35 to 44 minutes', '45 to 59 minutes', '60 minutes or more'];
                        var x_ticktext = ['Under 10 mins.', '10 to 14 mins.', '15 to 19 mins.', '20 to 24 mins.', '25 to 29 mins.', '30 to 34 mins.', '35 to 44 mins.', '45 to 59 mins.', '60 mins. or more'];
                        
                        
                        var title_text = `<b>Travel Times for Workers 16 and Older, ${selected_year}</b>`;
                    }

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'All Workers',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(229,216,189)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Male Workers',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(179,205,227)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    data3 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y3_array,
                        name: 'Female Workers',
                        'text': y3_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(244,202,228)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3];
                    
                }

                if ( selected_submeasure.startsWith("WorkHours") && selected_submeasure.includes("USUALHOURS_LONG") ) {
                    var y1_array = my_array.map(({value_TOTAL}) => value_TOTAL);
                    var y2_array = my_array.map(({value_MALE}) => value_MALE);
                    var y3_array = my_array.map(({value_FEMALE}) => value_FEMALE);
                    
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;

                    var xaxis_standoff = 20;
                    
                    var y1_text = y1_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                    });
                    var y2_text = y2_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                    });
                    var y3_text = y3_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                    });

                    var xaxis_title_text = '<b>Usual Hours Worked Weekly</b>';
                    
                    var yaxis_title_text = '<b>Number of Workers</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                    var x_tickvals = ['Usually worked 35 hours or more per week', 'Usually worked 15 to 34 hours per week', 'Usually worked 1 to 14 hours per week'];
                    var x_ticktext = ['35 hours or<br>more per week', '15 to 34 hours<br>per week', '1 to 14 hours<br>per week'];
                    
                    var title_text = `<b>Civilian Employed Workers by Usual Hours Worked, ${selected_year}</b>`;

                    data1 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y1_array,
                        name: 'All Workers',
                        'text': y1_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(229,216,189)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    data2 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y2_array,
                        name: 'Male Workers',
                        'text': y2_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(179,205,227)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    data3 = {
                        'type': 'bar',
                        'x': x_array,
                        'y': y3_array,
                        name: 'Female Workers',
                        'text': y3_text,
                        'textposition': 'auto',
                        'marker': {'line': {'color': '#111111', 'width': 1.5},
                                'color': 'rgb(244,202,228)'
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3];
                }

                if ( selected_submeasure.startsWith("WorkHours") && selected_submeasure.includes("MEANHOURS_LONG") ) {
                    var y_array = my_array.map(({value}) => value);
                        
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "<br>hours</b>";
                    });

                    var xaxis_title_text = '<b></b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                    var xlabels_size = 12;
                    var xaxis_standoff = 20;
                    
                    var yaxis_title_text = '<b>Mean Hours Worked Weekly</b>';
                    var title_text = `<b>Civilian Employed Workers by Mean Hours Worked, ${selected_year}</b>`;
                    var x_tickvals = ['Total', 'Male', 'Female'];
                    var x_ticktext = ['All<br>Workers', 'Male<br>Workers', 'Female<br>Workers'];

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': ['rgb(229,216,189)', 'rgb(179,205,227)', 'rgb(244,202,228)'],
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("EconomicMeasures")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                    });

                    var yaxis_title_text = '<b>Number of Civilian Workers</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    if (selected_submeasure.includes("INDUSTRY_LONG")){
                        var title_text = `<b>Civilian Workers by Industry, ${selected_year}</b>`;
                        var color_array = discrete_color_dict['Set3'];
                        
                        var x_tickvals = ['Agriculture, forestry, fishing and hunting, and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation and warehousing, and utilities', 'Information', 'Finance and insurance, and real estate and rental and leasing', 'Professional, scientific, and management, and administrative and waste management services', 'Educational services, and health care and social assistance', 'Arts, entertainment, and recreation, and accommodation and food services', 'Other services, except public administration', 'Public administration'];
                        var x_ticktext = ['Agriculture, forestry,<br>fishing, hunting<br>and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation,<br>warehousing,<br>utilities', 'Information', 'Finance, insurance,<br>real estate, rental<br>and leasing', 'Professional, scientific,<br>management, admin.,<br>waste management', 'Education,<br>healthcare,<br>social assistance', 'Arts, entertainment,<br>recreation, shelter,<br>and food', 'Other services', 'Public<br>administration'];
                        var xlabels_size = 8;
                    
                    } else if (selected_submeasure.includes("OCCUPATION")){
                        var title_text = `<b>Civilian Workers by Occupation, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Occupation</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Management, business, science, and arts occupations', 'Service occupations', 'Sales and office occupations', 'Natural resources, construction, and maintenance occupations', 'Production, transportation, and material moving occupations'];
                        var x_ticktext = ['Managerial,<br>business,<br>science, and arts', 'Services', 'Sales and office', 'Natural resources,<br>construction,<br>maintenance', 'Production,<br>transportation,<br>material moving'];
                        var xlabels_size = 11;
                        var xaxis_standoff = 20;
                    
                    } else if (selected_submeasure.includes("CLASS")){
                        var title_text = `<b>Civilian Workers by Sector, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Sector</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Private wage and salaried workers', 'Government workers', 'Self-employed in own/unincorporated business workers', 'Unpaid family workers'];
                        var x_ticktext = ['Private wage and<br>salaried workers', 'Government<br>workers', 'Self-employed<br>workers', 'Unpaid family<br>workers'];
                        var xlabels_size = 12;
                        var xaxis_standoff = 20;
                        
                    } else if (selected_submeasure.includes("EARNINGS")){
                        var title_text = `<b>Median Earnings for All Civilian Workers by Industry, ${selected_year}</b>`;
                        if (selected_submeasure.includes("FULL")){
                            var title_text = `<b>Median Earnings for Full-Time Civilian Workers by Industry, ${selected_year}</b>`;
                        }
                        var color_array = discrete_color_dict['Set3'];

                        var yaxis_tickprefix = '$';
                        var y_array = my_array.map(({value_TOTAL}) => value_TOTAL);

                        var ystr_array = my_array.map(({value_TOTAL_string}) => value_TOTAL_string);
                        var text = ystr_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                        });
                        var yaxis_title_text = '<b>Earnings ($)</b>';
                        
                        var x_tickvals = ['Agriculture, forestry, fishing and hunting, and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation and warehousing, and utilities', 'Information', 'Finance and insurance, and real estate and rental and leasing', 'Professional, scientific, and management, and administrative and waste management services', 'Educational services, and health care and social assistance', 'Arts, entertainment, and recreation, and accommodation and food services', 'Other services, except public administration', 'Public administration'];
                        var x_ticktext = ['Agriculture, forestry,<br>fishing, hunting<br>and mining', 'Construction', 'Manufacturing', 'Wholesale trade', 'Retail trade', 'Transportation,<br>warehousing,<br>utilities', 'Information', 'Finance, insurance,<br>real estate, rental<br>and leasing', 'Professional, scientific,<br>management, admin.,<br>waste management', 'Education,<br>healthcare,<br>social assistance', 'Arts, entertainment,<br>recreation, shelter,<br>and food', 'Other services', 'Public<br>administration'];
                        var xlabels_size = 8;
                    
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("Population")  ) {
                    var y_array = my_array.map(({value}) => value);
                    var xlabels_size;
                    var x_ticktext;
                    var x_tickvals;
                    
                    var text = y_array.map(function(item) {
                        return "<b style='color:#112A46; font-size:12px;'>" + item + "</b>";
                    });

                    var yaxis_title_text = '<b>Population</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';

                    if (selected_submeasure.includes("RACE")){
                        var title_text = `<b>Population by Race, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['White', 'Black or African American', 'American Indian and Alaska Native', 'Asian', 'Native Hawaiian and Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino (of any race)', 'White alone, not Hispanic or Latino'];
                        var x_ticktext = ['White', 'Black or<br>African American', 'American Indian<br>and Alaska Native', 'Asian', 'Native Hawaiian and<br>Other Pacific Islander', 'Some other race', 'Two or more races', 'Hispanic or Latino<br>(of any race)', 'White alone, not<br>Hispanic or Latino'];
                        var xlabels_size = 9;
                    
                    } else if (selected_submeasure.includes("ASIAN")){
                        var title_text = `<b>Asian Population, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Asian Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Asian Indian', 'Chinese', 'Filipino', 'Japanese', 'Korean', 'Vietnamese', 'Other Asian'];
                        var x_ticktext = ['Asian<br>Indian', 'Chinese', 'Filipino', 'Japanese', 'Korean', 'Vietnamese', 'Other<br>Asian'];
                        var xlabels_size = 13;
                        var xaxis_standoff = 20;
                    
                    } else if (selected_submeasure.includes("INDIGENOUS")){
                        var title_text = `<b>American Indian and Alaska Native Population, ${selected_year}</b>`;
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Cherokee', 'Chippewa', 'Navajo', 'Sioux', 'Aztec', 'Blackfeet Tribe of the Blackfeet Indian Reservation of Montana', 'Maya', 'Native Village of Barrow Inupiat Traditional Government', 'Navajo Nation', 'Nome Eskimo Community', 'Other American Indian and Alaska Native'];
                        var x_ticktext = ['Cherokee', 'Chippewa', 'Navajo', 'Sioux', 'Aztec', 'Blackfeet Tribe of the<br>Blackfeet Indian<br>Reservation of Montana', 'Maya', 'Native Village of<br>Barrow Inupiat<br>Traditional Government', 'Navajo Nation', 'Nome Eskimo<br>Community', 'Other American Indian<br>and Alaska Native'];
                        var xlabels_size = 9;
                        
                    } else if (selected_submeasure.includes("HISPANICLATINO")){
                        var title_text = `<b>Hispanic/Latino Population, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Hispanic/Latino Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Mexican', 'Puerto Rican', 'Cuban', 'Other Hispanic or Latino'];
                        var x_ticktext = ['Mexican', 'Puerto Rican', 'Cuban', 'Other Hispanic/<br>Latino'];
                        var xlabels_size = 14;
                        var xaxis_standoff = 20;
                    
                    } else if (selected_submeasure.includes("NATIVEHAWAIIANPACIFICISLANDER")){
                        var title_text = `<b>Native Hawaiian and Pacific Islander Population, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Native Hawaiian and Pacific Islander Racial Categories</b>';
                        var color_array = discrete_color_dict['Pastel2'];
                        
                        var x_tickvals = ['Native Hawaiian', 'Guamanian or Chamorro', 'Samoan', 'Other Pacific Islander', 'Chamorro', 'Other Native Hawaiian or Pacific Islander'];
                        var x_ticktext = ['Native Hawaiian', 'Guamanian or<br>Chamorro', 'Samoan', 'Other Pacific<br>Islander', 'Chamorro', 'Other Native Hawaiian<br>or Pacific Islander'];
                        var xlabels_size = 12;
                        var xaxis_standoff = 17;
                        
                    } else if (selected_submeasure.includes("_AGE_")){
                        var title_text = `<b>Population by Age Demographic, ${selected_year}</b>`;
                        var xaxis_title_text = '<b>Age Demographics</b>';
                        var color_array = discrete_color_dict['Blues'];
                        
                        var x_tickvals = ['Under 5', '5-9', '10-14', '15-19', '20-24', '25-34', '35-44', '45-54', '55-59', '60-64', '65-74', '75-84', '85+'];
                        var x_ticktext = ['Under 5', '5-9', '10-14', '15-19', '20-24', '25-34', '35-44', '45-54', '55-59', '60-64', '65-74', '75-84', '85+'];
                        var xlabels_size = 10;
                        var xaxis_standoff = 20;
                    }

                    var data = [{
                        'type': 'bar',
                        'x': x_array,
                        'y': y_array,
                        'text': text,
                        'textposition': 'auto',
                        'marker': {'color': color_array,
                                'line': {'color': '#111111', 'width': 1.5}
                                },
                        'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    }];
                    
                }

                if ( selected_submeasure.startsWith("Education") ) {
                    if ( selected_submeasure.includes("_AGE_") || selected_submeasure.includes("_RACE_") ) {
                        var y1_array = my_array.map(({value_MALE}) => value_MALE);
                        var y2_array = my_array.map(({value_FEMALE}) => value_FEMALE);
                        
                        var xlabels_size;
                        var x_ticktext;
                        var x_tickvals;
    
                        var xaxis_standoff = 20;
    
                        var xaxis_title_text = '<b>Educational Attainment</b>';
                        
                        var yaxis_title_text = '<b>Number of Individuals</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var x_tickvals = ['Less than 9th grade', '9th to 12th grade, no diploma', 'Less than high school diploma', 'High school graduate (includes equivalency)', 'Some college, no degree', "Some college or associate's degree", "Associate's degree", "Bachelor's degree", 'Graduate or professional degree', "Bachelor's degree or higher"];
                        var x_ticktext = ['Less than<br>9th grade', '9th to 12th grade<br>(No diploma)', 'Less than high<br>school graduate', 'High school graduate<br>(or equivalent)', 'Some college<br>(No degree)', "Some college or<br>associate's degree", "Associate's<br>degree", "Bachelor's<br>degree", 'Graduate or<br>professional<br>degree', "Bachelor's degree<br>or higher"];
                        
                        if ( selected_submeasure.includes("_AGE_") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:9px;'>" + item + "</b>";
                            });
                            var xlabels_size = 10;
                        }
                        if ( selected_submeasure.includes("_RACE_") ) {
                            var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var y2_text = y2_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:10px;'>" + item + "</b>";
                            });
                            var xlabels_size = 11;
                        }
                        
                        var title_text = `<b>Individuals by Educational Attainment, ${selected_year}</b>`;
                        
                        data1 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y1_array,
                            name: 'Men',
                            'text': y1_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': 'rgb(179,205,227)'
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        data2 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y2_array,
                            name: 'Women',
                            'text': y2_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': 'rgb(244,202,228)'
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        var data = [data1, data2];
                    }

                    if ( selected_submeasure.includes("CITIZENSHIP") ) {
                        var y1_array = my_array.map(({value_BORNINSTATE}) => value_BORNINSTATE);
                        var y2_array = my_array.map(({value_BORNOUTSTATE}) => value_BORNOUTSTATE);
                        var y3_array = my_array.map(({value_NATIVEOUTSIDE}) => value_NATIVEOUTSIDE);
                        var y4_array = my_array.map(({value_FOREIGN}) => value_FOREIGN);

                        var y1_text = y1_array.map(function(item) {
                                return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                            });
                        var y2_text = y2_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                        });
                        var y3_text = y3_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                        });
                        var y4_text = y4_array.map(function(item) {
                            return "<b style='color:#112A46; font-size:8px;'>" + item + "</b>";
                        });
                        
                        var xlabels_size = 9;
                        var x_ticktext;
                        var x_tickvals;
    
                        var xaxis_standoff = 10;
    
                        var xaxis_title_text = '<b>Educational Attainment</b>';
                        
                        var yaxis_title_text = '<b>Number of Individuals</b>';
                        var yaxis_tickprefix = '';
                        var yaxis_ticksuffix = '';
                        var x_tickvals = ['Less than high school graduate', 'High school graduate (includes equivalency)', "Some college or associate's degree", "Bachelor's degree", 'Graduate or professional degree'];
                        var x_ticktext = ['Less than high<br>school graduate', 'High school graduate<br>(or equivalent)', "Some college or<br>associate's degree", "Bachelor's<br>degree", 'Graduate or<br>professional<br>degree'];
                        
                        var title_text = `<b>Individuals by Educational Attainment, ${selected_year}</b>`;
                        
                        data1 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y1_array,
                            name: 'Born in-state',
                            'text': y1_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': discrete_color_dict['Pastel2'][0]
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        data2 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y2_array,
                            name: 'Born out-of-state',
                            'text': y2_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': discrete_color_dict['Pastel2'][1]
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };

                        data3 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y3_array,
                            name: 'Native (born<br>outside the U.S.)',
                            'text': y3_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': discrete_color_dict['Pastel2'][2]
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };

                        data4 = {
                            'type': 'bar',
                            'x': x_array,
                            'y': y4_array,
                            name: 'Foreign-born',
                            'text': y4_text,
                            'textposition': 'auto',
                            'marker': {'line': {'color': '#111111', 'width': 1.5},
                                    'color': discrete_color_dict['Pastel2'][3]
                                    },
                            'textfont': {'shadow': '1px 1px 20px #FEF9F3'},
                            'hoverinfo': 'none',
                            'hovertemplate': null
                        };
    
                        var data = [data1, data2, data3, data4];
                    }
                }


                

                
                
        
                var layout = {
                    'margin': {'b': 100, 't': 100, 'r': 80},
                    'xaxis': {'title': {'text': xaxis_title_text, 'standoff': xaxis_standoff},
                            'tickfont': {'size': xlabels_size},
                            'tickvals': x_tickvals,
                            'ticktext': x_ticktext
                            },
                    'yaxis': {'title': {'text': yaxis_title_text, 'standoff': 10},
                            'ticklabelstandoff': 5,
                            'tickprefix': yaxis_tickprefix,
                            'ticksuffix': yaxis_ticksuffix,
                            },
                    'barmode': barmode,
                    'paper_bgcolor': '#FEF9F3',
                    'plot_bgcolor': '#FEF9F3',
                    'title': {'text': title_text,
                            'x': 0.05,
                            'subtitle': {'text': `${tract_name}, ${city_string}`}
                            }
                };
            }

            if ( selected_submeasure.includes("TIME") ) {
                var my_array = tooltip_data.filter(item => item['TRACT'] == tract_name);
                var x_array = my_array.map(({YEAR}) => YEAR);


                if ( selected_submeasure.startsWith("ContractRent") ) {
                    var y1_array = my_array.map(({Lowercontractrentquartile}) => Lowercontractrentquartile);
                    var y2_array = my_array.map(({Mediancontractrent}) => Mediancontractrent);
                    var y3_array = my_array.map(({Uppercontractrentquartile}) => Uppercontractrentquartile);
                    
                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': '25th Percentile<br>Contract Rent',
                        'line': {'color': '#E3242B', 'dash': 'dashdot'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': 'Median Contract<br>Rent',
                        'line': {'color': '#990F02'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    var data3 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y3_array,
                        'name': '75th Percentile<br>Contract Rent',
                        'line': {'color': '#551606', 'dash': 'dashdot'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
    
                    var data = [data3, data2, data1];
                    
                    var yaxis_title_text = '<b>Contract Rents</b>';
                    var yaxis_tickprefix = '$';
                    var yaxis_ticksuffix = '';
                    
                    var title_text = `<b>Contract Rents, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;

                }

                

                if ( selected_submeasure.startsWith("RentBurden") && !selected_submeasure.includes("AGE") && !selected_submeasure.includes("INCOME") ) {
                    var y1_array = my_array.map(({ESTIMATE_Totalrenters_RentBurden}) => ESTIMATE_Totalrenters_RentBurden);
                    var y2_array = my_array.map(({ESTIMATE_Totalrenters_SevereRentBurden}) => ESTIMATE_Totalrenters_SevereRentBurden);
                    
                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': 'Rent Burden',
                        'line': {'color': discrete_color_dict['Reds_2'][0]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': 'Severe Rent Burden',
                        'line': {'color': discrete_color_dict['Reds_2'][1]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
    
                    var data = [data1, data2];
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Rent Burden Severity, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                }

                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("AGE") ) {
                    var y1_array = my_array.map(({ESTIMATE_Totalrenters_AGE_RentBurden}) => ESTIMATE_Totalrenters_AGE_RentBurden);
                    var y2_array = my_array.map(({ESTIMATE_Totalrenters_AGE_15to24_RentBurden}) => ESTIMATE_Totalrenters_AGE_15to24_RentBurden);
                    var y3_array = my_array.map(({ESTIMATE_Totalrenters_AGE_25to34_RentBurden}) => ESTIMATE_Totalrenters_AGE_25to34_RentBurden);
                    var y4_array = my_array.map(({ESTIMATE_Totalrenters_AGE_35to64_RentBurden}) => ESTIMATE_Totalrenters_AGE_35to64_RentBurden);
                    var y5_array = my_array.map(({ESTIMATE_Totalrenters_AGE_65andOlder_RentBurden}) => ESTIMATE_Totalrenters_AGE_65andOlder_RentBurden);

                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': 'Overall',
                        'line': {'color': discrete_color_dict['Okabe_8'][0]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': '15 to 24',
                        'line': {'color': discrete_color_dict['Okabe_8'][1]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data3 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y3_array,
                        'name': '25 to 34',
                        'line': {'color': discrete_color_dict['Okabe_8'][2]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data4 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y4_array,
                        'name': '35 to 64',
                        'line': {'color': discrete_color_dict['Okabe_8'][3]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data5 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y5_array,
                        'name': '65 and older',
                        'line': {'color': discrete_color_dict['Okabe_8'][5]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3, data4, data5];
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Rent-Burdened Renters by Age, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;

                }
                
                if ( selected_submeasure.startsWith("RentBurden") && selected_submeasure.includes("INCOME") ) {
                    var y1_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_RentBurden);
                    var y2_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_Lessthan10000_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_Lessthan10000_RentBurden);
                    var y3_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_10000to19999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_10000to19999_RentBurden);
                    var y4_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_20000to34999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_20000to34999_RentBurden);
                    var y5_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_35000to49999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_35000to49999_RentBurden);
                    var y6_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_50000to74999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_50000to74999_RentBurden);
                    var y7_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_75000to99999_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_75000to99999_RentBurden);
                    var y8_array = my_array.map(({ESTIMATE_Totalrenters_INCOMECATEGORY_100000ormore_RentBurden}) => ESTIMATE_Totalrenters_INCOMECATEGORY_100000ormore_RentBurden);

                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': 'Overall',
                        'line': {'color': discrete_color_dict['Okabe_8'][0]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': 'Less than $10k',
                        'line': {'color': discrete_color_dict['Okabe_8'][1]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data3 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y3_array,
                        'name': '$10k to 19.9k',
                        'line': {'color': discrete_color_dict['Okabe_8'][2]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data4 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y4_array,
                        'name': '$20k to 34.9k',
                        'line': {'color': discrete_color_dict['Okabe_8'][3]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data5 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y5_array,
                        'name': '$35k to 49.9k',
                        'line': {'color': discrete_color_dict['Okabe_8'][4]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data6 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y6_array,
                        'name': '$50k to 74.9k',
                        'line': {'color': discrete_color_dict['Okabe_8'][5]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data7 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y7_array,
                        'name': '$75k to 99.9k',
                        'line': {'color': discrete_color_dict['Okabe_8'][6]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data8 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y8_array,
                        'name': '$100k or more',
                        'line': {'color': discrete_color_dict['Okabe_8'][7]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data = [data1, data2, data3, data4, data5, data6, data7, data8];
                    
                    var yaxis_title_text = '<b>Percentage of Renters</b>';
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                    
                    var title_text = `<b>Rent-Burdened Renters by Income, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("RACE_TIME")  ) {
                    var y1_array = my_array.map(({Overall16andOlder}) => Overall16andOlder);
                    var y2_array = my_array.map(({White}) => White);
                    var y3_array = my_array.map(({BlackorAfricanAmerican}) => BlackorAfricanAmerican);
                    var y4_array = my_array.map(({AmericanIndianandAlaskaNative}) => AmericanIndianandAlaskaNative);
                    var y5_array = my_array.map(({Asian}) => Asian);
                    var y6_array = my_array.map(({NativeHawaiianandOtherPacificIslander}) => NativeHawaiianandOtherPacificIslander);
                    var y7_array = my_array.map(({Someotherrace}) => Someotherrace);
                    var y8_array = my_array.map(({Twoormoreraces}) => Twoormoreraces);
                    var y9_array = my_array.map(({HispanicorLatinooriginofanyrace}) => HispanicorLatinooriginofanyrace);
                    var y10_array = my_array.map(({WhitenotHispanicorLatino}) => WhitenotHispanicorLatino);

                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': 'Overall (16 and Older)',
                        'line': {'color': discrete_color_dict['G10'][0]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': 'White',
                        'line': {'color': discrete_color_dict['G10'][1]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data3 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y3_array,
                        'name': 'Black or African<br>American',
                        'line': {'color': discrete_color_dict['G10'][2]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data4 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y4_array,
                        'name': 'American Indian and<br>Alaska Native',
                        'line': {'color': discrete_color_dict['G10'][3]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data5 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y5_array,
                        'name': 'Asian',
                        'line': {'color': discrete_color_dict['G10'][4]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data6 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y6_array,
                        'name': 'Native Hawaiian and<br>Other Pacific Islander',
                        'line': {'color': discrete_color_dict['G10'][5]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data7 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y7_array,
                        'name': 'Some other race',
                        'line': {'color': discrete_color_dict['G10'][6]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data8 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y8_array,
                        'name': 'Two or more races',
                        'line': {'color': discrete_color_dict['G10'][7]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data9 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y9_array,
                        'name': 'Hispanic or Latino<br>(of any race)',
                        'line': {'color': discrete_color_dict['G10'][8]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data10 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y10_array,
                        'name': 'White, not Hispanic<br>or Latino',
                        'line': {'color': discrete_color_dict['G10'][9]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Race, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Race, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Race, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    }
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("SEX_TIME")  ) {
                    var y1_array = my_array.map(({Overall20to64}) => Overall20to64);
                    var y2_array = my_array.map(({Male}) => Male);
                    var y3_array = my_array.map(({Female}) => Female);
                    var y4_array = my_array.map(({FemaleWithchildrenunder6yearsold}) => FemaleWithchildrenunder6yearsold);
                    var y5_array = my_array.map(({FemaleWithchildrenunder18yearsold}) => FemaleWithchildrenunder18yearsold);
                    var y6_array = my_array.map(({FemaleWithchildrenunder17yearsold}) => FemaleWithchildrenunder17yearsold);
                    var y7_array = my_array.map(({FemaleWithchildren6to17yearsold}) => FemaleWithchildren6to17yearsold);

                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': 'Overall (20 to 64)',
                        'line': {'color': discrete_color_dict['D3_7'][0]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': 'Male',
                        'line': {'color': discrete_color_dict['D3_7'][1]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data3 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y3_array,
                        'name': 'Female',
                        'line': {'color': discrete_color_dict['D3_7'][2]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data4 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y4_array,
                        'name': 'Female (With children<br>under 6 years old)',
                        'line': {'color': discrete_color_dict['D3_7'][3]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data5 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y5_array,
                        'name': 'Female (With children<br>under 18 years old)',
                        'line': {'color': discrete_color_dict['D3_7'][4]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data6 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y6_array,
                        'name': 'Female (With children<br>under 17 years old)',
                        'line': {'color': discrete_color_dict['D3_7'][5]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data7 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y7_array,
                        'name': 'Female (With children<br>6 to 17 years old)',
                        'line': {'color': discrete_color_dict['D3_7'][6]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3, data4, data5, data6, data7];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Sex, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Sex, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Sex, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    }
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                }

                if ( selected_submeasure.startsWith("EmploymentStatistics") && selected_submeasure.includes("EDUCATIONALSTATUS_TIME")  ) {
                    var y1_array = my_array.map(({Overall25to64}) => Overall25to64);
                    var y2_array = my_array.map(({Lessthanhighschoolgraduate}) => Lessthanhighschoolgraduate);
                    var y3_array = my_array.map(({Highschoolgraduateincludesequivalency}) => Highschoolgraduateincludesequivalency);
                    var y4_array = my_array.map(({Somecollegeorassociatesdegree}) => Somecollegeorassociatesdegree);
                    var y5_array = my_array.map(({Bachelorsdegreeorhigher}) => Bachelorsdegreeorhigher);

                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': 'Overall (25 to 64)',
                        'line': {'color': discrete_color_dict['D3_5'][0]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': 'Less than high<br>school graduate',
                        'line': {'color': discrete_color_dict['D3_5'][1]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data3 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y3_array,
                        'name': 'High school graduate<br>(or equivalent)',
                        'line': {'color': discrete_color_dict['D3_5'][2]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data4 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y4_array,
                        'name': "Some college or<br>associate's degree",
                        'line': {'color': discrete_color_dict['D3_5'][3]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data5 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y5_array,
                        'name': "Bachelor's degree<br>or higher",
                        'line': {'color': discrete_color_dict['D3_5'][5]},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3, data4, data5];

                    if (selected_submeasure.includes("UNEMP")){
                        var yaxis_title_text = '<b>Unemployment Rate</b>';
                        var title_text = `<b>Unemployment Rates by Educational Attainment, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("LFPR")){
                        var yaxis_title_text = '<b>Labor Force Participation Rate</b>';
                        var title_text = `<b>Labor Force Participation Rates by Educational Attainment,<br>${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    } else if (selected_submeasure.includes("EPOP")){
                        var yaxis_title_text = '<b>Employment-to-Population Ratio</b>';
                        var title_text = `<b>Employment-to-Population Ratios by Educational Attainment,<br>${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    }
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '%';
                }

                if ( selected_submeasure.startsWith("WorkHours") && selected_submeasure.includes("MEANHOURS_TIME")  ) {
                    var y1_array = my_array.map(({Total}) => Total);
                    var y2_array = my_array.map(({Male}) => Male);
                    var y3_array = my_array.map(({Female}) => Female);

                    var data1 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y1_array,
                        'name': 'All<br>Workers',
                        'line': {'color': 'rgb(194, 163, 99)'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data2 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y2_array,
                        'name': 'Male<br>Workers',
                        'line': {'color': 'rgb(90, 146, 194)'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };

                    var data3 = {
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'x': x_array,
                        'y': y3_array,
                        'name': 'Female<br>Workers',
                        'line': {'color': 'rgb(221, 91, 172)'},
                        'hoverinfo': 'none',
                        'hovertemplate': null
                    };
                    
                    var data = [data1, data2, data3];

                    var yaxis_title_text = '<b>Mean Hours Worked Weekly</b>';
                    var title_text = `<b>Mean Hours Worked Weekly, ${Math.min(...x_array)} to ${Math.max(...x_array)}</b>`;
                    
                    var yaxis_tickprefix = '';
                    var yaxis_ticksuffix = '';
                }
                
                var layout = {
                    'margin': {'b': 100, 't': 100, 'r': 80},
                    'xaxis': {'title': {'text': '<b>Year</b>', 'standoff': 20},
                            'showgrid': false,
                            'tick0': Math.min(...x_array),
                            'dtick': 2
                            },
                    'yaxis': {'title': {'text': yaxis_title_text, 'standoff': 10},
                            'ticklabelstandoff': 5,
                            'gridcolor': '#E0E0E0',
                            'tickprefix': yaxis_tickprefix,
                            'ticksuffix': yaxis_ticksuffix,
                            },
                    'paper_bgcolor': '#FEF9F3',
                    'plot_bgcolor': '#FEF9F3',
                    'title': {'text': title_text,
                            'x': 0.05, 'y': 0.94,
                            'subtitle': {'text': `${tract_name}, ${city_string}`}
                            }
                };
            
            }

            var bbox = hoverData['points']['0']['bbox'];
    
            var fig = {'data': data, 'layout': layout};
    
            return [true, fig, bbox];
        }
    }
}