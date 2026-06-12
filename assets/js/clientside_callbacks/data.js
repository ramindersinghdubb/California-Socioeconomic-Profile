window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside_data_callbacks = {
    /**
     * Retrieve the masterfile data for the given city, calendar year,
     * and measure.
     * 
     * @param {Number} selected_year The selected calendar year.
     * @param {String} selected_place The selected city/place.
     * @param {String} selected_measure The selected measure.
     * @returns {Array} An array consisting of the masterfile data.
     */
    masterfile_data: async function(selected_year, selected_place, selected_measure) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_SocioeconomicIndicators/${selected_year}/${selected_measure}_${selected_place}_${selected_year}.json`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    },

    /**
     * Retrieve the tooltip data for the given city, calendar year, and
     * submeasure.
     * 
     * @param {Number} selected_year The selected calendar year.
     * @param {String} selected_place The selected city/place.
     * @param {String} selected_submeasure The selected submeasure (to-be-plotted in
     * the tooltip).
     * @returns {Array} An array consisting of the submeasure/tooltip data.
     */
    tooltip_data: async function(selected_year, selected_place, selected_submeasure) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_SocioeconomicIndicators/${selected_year}/${selected_submeasure}_${selected_place}_${selected_year}.json`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    },

    /**
     * Retrieve the longitudal and latitudinal coordinates for the approximate center
     * points of each city/place for the selected calendar year.
     * 
     * @param {Number} selected_year The selected calendar year.
     * @returns {Array} An array consisting of the center-points for each city/place.
     */
    mapfile_center_points_data: async function(selected_year) {
        const url = `https://raw.githubusercontent.com/ramindersinghdubb/datasets/refs/heads/main/SoCal_CensusTract_Mapfiles/SoCal_LatLongPoints_${selected_year}.json`;
        const response = await fetch(url);
        const data = await response.json();
        return data;
    },
    
    /**
     * Redundancy for tooltip data if the submeasure is not selected.
     * 
     * @param {String} selected_submeasure The selected submeasure.
     * @returns Null
     */
    tooltip_redundancy: function(selected_submeasure) {
        if (selected_submeasure === undefined || selected_submeasure === null) {
            return 'hidethis';
        } else {
            return '';
        }
    }
}