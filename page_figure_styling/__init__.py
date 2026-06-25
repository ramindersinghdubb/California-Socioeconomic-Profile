"""
HTML/styling components for the `dash.dcc.Graph` figure.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

# Registry
from page_figure_styling._tool_ContractRent import ContractRentTooltip
from page_figure_styling._tool_EconomicMeasures import EconomicMeasuresTooltip
from page_figure_styling._tool_Education import EducationTooltip
from page_figure_styling._tool_EmploymentStatistics import EmploymentStatisticsTooltip
from page_figure_styling._tool_FoodStamps import FoodStampsTooltip
from page_figure_styling._tool_HealthInsuranceCoverage import HealthInsuranceCoverageTooltip
from page_figure_styling._tool_HouseholdIncome import HouseholdIncomeTooltip
from page_figure_styling._tool_HousingUnitsandOccupancy import HousingUnitsandOccupancyTooltip
from page_figure_styling._tool_Population import PopulationTooltip
from page_figure_styling._tool_Poverty import PovertyTooltip
from page_figure_styling._tool_RentBurden import RentBurdenTooltip
from page_figure_styling._tool_TransportationMethodstoWork import TransportationMethodstoWorkTooltip
from page_figure_styling._tool_WorkHours import WorkHoursTooltip
from page_figure_styling._abc import TooltipFigureMetaABC

from page_figure_styling.choropleth_metadata import ChoroplethMapInterface
from page_figure_styling.tooltip_figure import TooltipFigureInterface

__all__ = [
    'ChoroplethMapInterface',
    'TooltipFigureInterface',
]