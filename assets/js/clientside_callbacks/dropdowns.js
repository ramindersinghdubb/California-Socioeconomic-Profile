window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside_dropdowns = {
    /**
     * Update the available options for cities/places based on the selected year.
     * 
     * @param {Number} selected_year The selected calendar year.
     * @param {Map} year_place_options A map such such that keys are years, and values
     * are the available options for cities/places.
     * @returns {Array} The array of available options for cities/places.
     */
    place_options_function: function(selected_year, year_place_options) {
        return year_place_options[selected_year];
    },

    /**
     * Update the supported calendar years (given the selected city and selected
     * measure).
     * 
     * @param {String} selected_place The selected place/city.
     * @param {String} selected_measure The selected measure.
     * @param {Map} place_years_options A map such that keys are places/cities, and
     * values are the supported calendar years.
     * @param {Map} measure_year_options A map such that keys are measures, and values
     * are the supported calendar years.
     * @returns {Array} The array of supported calendar years.
     */
    year_options_function: function(selected_place, selected_measure, place_years_options, measure_year_options) {
        var years_options = place_years_options[selected_place];

        if ( ['HealthInsuranceCoverage', 'Poverty', 'FoodStamps'].includes(selected_measure) ) {
            var years_options = measure_year_options[selected_measure];
        }

        return years_options
    },

    /**
     * Update the supported measures (given the selected calendar year).
     * 
     * @param {Number} selected_year The selected calendar year.
     * @param {Map} year_measures_options A map such that keys are calendar years, and values
     * are the supported measures.
     * @returns {Array} The array of supported measure options.
     */
    measure_options_functions: function(selected_year, year_measures_options) {
        var measures_options = year_measures_options[selected_year];
        
        return measures_options;
    },
    
    /**
     * Given a measure, list the available submeasure options.
     * 
     * @param {String} selected_measure The selected measure.
     * @param {Map} submeasures_dict A map such that keys are measures, and values are the
     * submeasures.
     * @returns {Array} The array of supported submeasure options.
     */
    submeasure_options_function: function(selected_measure, submeasures_dict) {
        if (selected_measure) {
            return submeasures_dict[`${selected_measure}`];
        }
        return window.dash_clientside.no_update;
    }
}