"""
Tooltip metadata interface for the 'Education' category.
"""

import typing as t

import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC
from ingestion.utils import lettered_table



class EducationTooltip(TooltipFigureMetaABC, measure = 'Education'):
    """
    Tooltip metadata interface for the 'Education' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            # 'Educational Attainment by Citizenship Status': cls.EducationalAttainmentbyCitizenshipStatus,
            'Educational Attainment by Racial Status': cls.EducationalAttainmentbyRacialStatus,
            'Educational Attainment by Age': cls.EducationalAttainmentbyAge,
            'Educational Attainment by Sexual Orientation': cls.EducationalAttainmentbySexualOrientation,
        }
        return lambda_dict

        
    
    # @classmethod
    # def EducationalAttainmentbyCitizenshipStatus(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # Unavailable for only 2009 (B06009; has partial availability)



    @classmethod
    def EducationalAttainmentbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # Use C15002 tables (full availability)
        # 001E is the population total, 002E is the total for men, 007E is the total for women
        # 003E to 006E are the EA for men, 008E to 011E are the EA for women
        # All estimates are absolute estimates
        tbl_labs = [
            "White alone",
            "Black or African<br>American",
            "American Indian and<br>Alaska Native",
            "Asian",
            "Native Hawaiian and<br>Other Pacific Islander",
            "Some other race",
            "Two or more races",
            "White (not Hispanic<br>or Latino)",
            "Hispanic or Latino",
        ]
        tbls = [i + '_' for i in lettered_table('C15002')]

        edu_labs = cls.__get_four_edu_labels()

        dfs = []
        for tbl, tbl_lab in zip(tbls, tbl_labs):
            temp_df = df.copy(deep=True)
            temp_df['TOTAL'] = temp_df[f'{tbl}001E']

            pop_vars = [f'POPULAT_{i}' for i in edu_labs]
            for num, pop_var in zip([3, 4, 5, 6], pop_vars):
                totals = cls.generate_particular_variables(tbl, [num, num+5])
                temp_df[pop_var] = temp_df[totals].sum(axis=1)
            
            per_vars  = [f'PERCENT_{i}' for i in edu_labs]
            for per_var, pop_var in zip(per_vars, pop_vars):
                temp_df[per_var] = temp_df[pop_var].div(temp_df['TOTAL'], fill_value=np.nan).mul(100, fill_value=np.nan).round(1)
            
            temp_df = cls.get_long_df_values_populations(temp_df, per_vars, pop_vars, edu_labs, 'TOTAL')
            temp_df['RACIAL_STATUS'] = tbl_lab
            dfs.append(temp_df)

        df = pd.concat(dfs)

        colors = ['#F79256', '#FBD1A2', '#7DCFB6', '#00B2CA']
        color_discrete_map = dict(zip(edu_labs, colors))

        df['COLOR'] = df['VARIABLE'].map(color_discrete_map)
        df['EDU_TEXT'] = df['VARIABLE'].map(edu_labs)
        EDU_ATT_VAR = "<span style='font-family: Trebuchet MS, sans-serif; font-weight: 700;'>Educational<br>Attainment</span>"
        df.rename(columns={'VARIABLE': EDU_ATT_VAR}, inplace=True)

        metadata = {
            'dataframe': df,
            'x': 'RACIAL_STATUS',
            'y': 'VALUE',
            'color': EDU_ATT_VAR,
            'barmode': 'group',
            'color_discrete_map': color_discrete_map,
            'showlegend': True,
            'title': {
                'text': "<b style='font-size:20px;'>Educational Attainment by Racial Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Racial Status</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 8
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Percent of Population (%)</b>",
                    'standoff': 25
                },
                'ticklabelstandoff': 5,
                'ticksuffix': '%'
            },
            'marker': {
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            },
            'custom_data': ['POPULATION', 'TOTAL', 'RACIAL_STATUS', 'COLOR', 'EDU_TEXT'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{customdata[2]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b style='color: %{customdata[3]};font-size:12px;'>%{customdata[4]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Percent of Individuals: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Individuals: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Individuals (25 and older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata


    @classmethod
    def EducationalAttainmentbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # Use B15001 (full availability)
        # 001E is the population total
        # All estimates are absolute estimates
        age_labs = [
            "18 to 24",
            "25 to 34",
            "35 to 44",
            "45 to 64",
            "65 and Older",
        ]
        edu_labs = cls.__get_seven_edu_labels()

        dfs = []
        for age, m_idx, w_idx in zip(age_labs, range(3, 43, 8), range(44, 83, 8)):
            temp_df = df.copy(deep=True)
            age_totals = cls.generate_particular_variables('B15001_', [m_idx, w_idx])
            temp_df['TOTAL'] = temp_df[age_totals].sum(axis=1)

            pop_vars = [f'POPULAT_{i}' for i in edu_labs]
            for pop_var, m_step, w_step in zip(pop_vars, range(m_idx+1, m_idx+8), range(w_idx+1, w_idx+8)):
                pop_totals       = cls.generate_particular_variables('B15001_', [m_step, w_step])
                temp_df[pop_var] = temp_df[pop_totals].sum(axis=1)
            
            per_vars  = [f'PERCENT_{i}' for i in edu_labs]
            for per_var, pop_var in zip(per_vars, pop_vars):
                temp_df[per_var] = temp_df[pop_var].div(temp_df['TOTAL'], fill_value=np.nan).mul(100, fill_value=np.nan).round(1)

            temp_df = cls.get_long_df_values_populations(temp_df, per_vars, pop_vars, edu_labs, 'TOTAL')
            temp_df['AGE'] = age
            dfs.append(temp_df)

        df = pd.concat(dfs)

        colors = ["#011a4d","#255d8d","#499fcd","#86bca4","#c2d87a","#fece52","#feb94a"]
        color_discrete_map = dict(zip(edu_labs, colors))

        df['COLOR'] = df['VARIABLE'].map(color_discrete_map)
        df['EDU_TEXT'] = df['VARIABLE'].map(edu_labs)
        EDU_ATT_VAR = "<span style='font-family: Trebuchet MS, sans-serif; font-weight: 700;'>Educational<br>Attainment</span>"
        df.rename(columns={'VARIABLE': EDU_ATT_VAR}, inplace=True)

        metadata = {
            'dataframe': df,
            'x': 'AGE',
            'y': 'VALUE',
            'color': EDU_ATT_VAR,
            'barmode': 'group',
            'color_discrete_map': color_discrete_map,
            'showlegend': True,
            'title': {
                'text': "<b style='font-size:20px;'>Educational Attainment by Age</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Age Demographic</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Percent of Population (%)</b>",
                    'standoff': 25
                },
                'ticklabelstandoff': 5,
                'ticksuffix': '%'
            },
            'marker': {
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            },
            'custom_data': ['POPULATION', 'TOTAL', 'AGE', 'COLOR', 'EDU_TEXT'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{customdata[2]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b style='color: %{customdata[3]};font-size:12px;'>%{customdata[4]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Percent of Individuals: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Individuals: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Individuals (%{customdata[2]}): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def EducationalAttainmentbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # Use B15001 (full availability)
        sex_ori_labs = ["Men", "Women"]
        edu_labs = cls.__get_seven_edu_labels()

        dfs = []
        for sex_ori, idx in zip(sex_ori_labs, [2, 43]):
            temp_df = df.copy(deep=True)
            age_totals = cls.generate_particular_variables('B15001_', [idx])
            temp_df['TOTAL'] = temp_df[age_totals].sum(axis=1)

            pop_vars = [f'POPULAT_{i}' for i in edu_labs]
            for pop_var, step in zip(pop_vars, range(1, 8)):
                pop_totals       = cls.generate_particular_variables('B15001_', list(range(idx+1+step, idx+34+step, 8)))
                temp_df[pop_var] = temp_df[pop_totals].sum(axis=1)
            
            per_vars  = [f'PERCENT_{i}' for i in edu_labs]
            for per_var, pop_var in zip(per_vars, pop_vars):
                temp_df[per_var] = temp_df[pop_var].div(temp_df['TOTAL'], fill_value=np.nan).mul(100, fill_value=np.nan).round(1)

            temp_df = cls.get_long_df_values_populations(temp_df, per_vars, pop_vars, edu_labs, 'TOTAL')
            temp_df['SEXUAL_ORIENTATION'] = sex_ori
            dfs.append(temp_df)

        df = pd.concat(dfs)

        colors = ["#011a4d","#255d8d","#499fcd","#86bca4","#c2d87a","#fece52","#feb94a"]
        color_discrete_map = dict(zip(edu_labs, colors))

        df['COLOR'] = df['VARIABLE'].map(color_discrete_map)
        df['EDU_TEXT'] = df['VARIABLE'].map(edu_labs)
        EDU_ATT_VAR = "<span style='font-family: Trebuchet MS, sans-serif; font-weight: 700;'>Educational<br>Attainment</span>"
        df.rename(columns={'VARIABLE': EDU_ATT_VAR}, inplace=True)

        metadata = {
            'dataframe': df,
            'x': 'SEXUAL_ORIENTATION',
            'y': 'VALUE',
            'color': EDU_ATT_VAR,
            'barmode': 'group',
            'color_discrete_map': color_discrete_map,
            'showlegend': True,
            'title': {
                'text': "<b style='font-size:20px;'>Educational Attainment by Sexual Orientation</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:20px;'>Sexual Orientation</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 15
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Percent of Population (%)</b>",
                    'standoff': 25
                },
                'ticklabelstandoff': 5,
                'ticksuffix': '%'
            },
            'marker': {
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            },
            'custom_data': ['POPULATION', 'TOTAL', 'SEXUAL_ORIENTATION', 'COLOR', 'EDU_TEXT'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{customdata[2]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b style='color: %{customdata[3]};font-size:12px;'>%{customdata[4]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Percent of Individuals: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Individuals: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Individuals (%{customdata[2]}): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata


    @classmethod
    def __get_four_edu_labels(cls) -> t.Dict[str, str]:
        html_edu_labs = [
            "Less than HS<br>graduate",
            "HS graduate<br>or equivalent",
            "Some college<br>or associate's",
            "Bachelor's or<br>higher",
        ]
        text_edu_labs = [
            "Less than HS graduate",
            "High school graduate or equivalent",
            "Some college or associate's degree",
            "Bachelor's degree or higher",
        ]
        edu_labs = dict(zip(html_edu_labs, text_edu_labs))

        return edu_labs
    

    @classmethod
    def __get_seven_edu_labels(cls) -> t.Dict[str, str]:
        html_edu_labs = [
            "Less than 9th",
            "9th to 12th (no<br>diploma)",
            "HS graduate<br>or equivalent",
            "Some college (no<br>degree)",
            "Associate's",
            "Bachelor's",
            "Graduate or<br>professional",
        ]
        text_edu_labs = [
            "Less than than 9th grade",
            "9th to 12th grade (no diploma)",
            "High school graduate or equivalent",
            "Some college (no degree)",
            "Associate's degree",
            "Bachelor's degree",
            "Graduate or professional degree",
        ]
        edu_labs = dict(zip(html_edu_labs, text_edu_labs))

        return edu_labs


