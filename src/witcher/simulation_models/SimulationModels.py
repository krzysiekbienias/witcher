import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql
import os
import pandas as pd
from datetime import datetime


from witcher.simulation_models.SimulationEnvironment import SimulationEnvironment
from witcher.black_scholes_framework.pricing.AnalyticalPrice import EuropeanStyleOption, MarketEnvironment

from typing import TypeVar, Iterable, Tuple, Dict, List

HM = TypeVar("HM", bound=Dict)
DT = TypeVar('DT')  # declaration HM type


class GeometricBrownianMotion(SimulationEnvironment):

    def __init__(self,
                drift: float,
                volatility: float,
                initialisation_point: float,
                #######################
                 start_simulation_date: DT,
                 end_simulation_date: DT,
                 calendar: str = 'USA',
                 year_fraction_convention: str = 'Actual365',
                 frequency: str = "daily",
                 simulation_schema: str = "Exact_Solution",
                 **kwargs):
        self._drift = drift
        self._volatility = volatility
        self._simulation_schema = simulation_schema
        self._initialisation_point = initialisation_point
        super().__init__(start_simulation_date, end_simulation_date, calendar,
                         year_fraction_convention, frequency, **kwargs)
        
        risk_factor_array = self.runSimulation(simulation_schema=self._simulation_schema)
        
        # paths_metrics_dfs = self.getPathsMetrics(df=df_gbm_paths,
        #                                          t_quantiles_name=(
        #                                              'upper_quantile', 'bottom_quantile'),
        #                                          t_quantiles_values=(0.97, 0.03))
        # --------------
        # Region: Preparing Plots
        # ---------------
        # graph_representation = IOTools.plotUsingMatPlot(ts_df_list=[df_gbm_paths.iloc[:, :20],
        #                                                             paths_metrics_dfs],
        #                                                 ts_labels_list=["Paths", "Metrics"],
        #                                                 n_col=2,
        #                                                 n_row=1)
        # --------------
        # Region: Customize Plots
        # ---------------
        # graph_representation[1][0].set_facecolor('grey')
        # graph_representation[1][1].set_facecolor('pink')
        # graph_representation[1][1].legend(
        #     ['Upper Quantile', 'Bottom Quantile', 'Mean'])
        # os.chdir("../drop_point")
        # graph_representation[0].savefig("equity_paths_GBM_Model.png")
        # --------------
        # Region: Customize Plots
        # ---------------

        # --------------
        # End Region: Preparing Plots
        # ---------------

    def eulerDiscretisationSchema(self,
                                  simulation_dates:List[DT],
                                  simulation_grid:List[float],

                                  paths_number:int=1000) -> np.array:
        """
        Description
        -----------
        This function creates numpy array that represents modelled equity prices using Euler discretization schema.

        Parameters
        ----------
        path_number : int, optional
            number os scenarios, by default 1000

        Returns
        -------
        numpy arr
            array representing scenarios along defined timestep calendar. Rows represent simulation grid, column
        """
        dt = simulation_grid
        x_ip1 = np.zeros((paths_number, len(simulation_dates)))
        x_ip1[:, 0] = self._initialisation_point
        for t in range(1, len(x_ip1[0])):
            z = np.random.standard_normal(x_ip1)
            x_ip1[:, t] = +x_ip1[:, t - 1] * dt + \
                self._volatility * z * np.sqrt(dt)
        return np.transpose(x_ip1)

    def milsteinDiscretisationSchema(self,
                                    simulation_dates:List[DT],
                                  simulation_grid:List[float],

                                  paths_number:int=1000) -> np.array:
        """

        Description
        -----------
        This function creates numpy array that represents modelled equity behavior using Milstein discretization schema.



        Parameters
        ----------
        path_number : int, optional
            number os scenarios, by default 1000

        Returns
        -------
        np.array
            array representing scenarios along defined timestamp calendar
        """

        dt = simulation_grid
        x_ip1 = np.zeros((paths_number, len(simulation_grid)))  # create empty array #TODO to nie moze byc do scenario calendar tylko zalezec od obiektu o_gbmscenarios
        x_ip1[:, 0] = self._initialisation_point
        for t in range(1, len(x_ip1[0])):
            z = np.random.standard_normal(x_ip1)
            x_ip1[:, t] = +x_ip1[:, t - 1] * dt + self._volatility * \
                z * np.sqrt(dt) + 0.5 * self._volatility * (dt * z - dt)
        return np.transpose(x_ip1)

    def geometricBrownianMotion(self, 
                                  simulation_dates:List[DT],
                                  simulation_grid:List[float],
                                  paths_number:int=1000) -> np.array:
        """

        Parameters
        ----------
        paths_number : int, optional
            _description_, by default 1000

        Returns
        -------
        np.array
            _description_
        """

        dt = simulation_grid
        gbm_model = np.zeros((paths_number, len(
            simulation_dates)))  # create empty array #TODO to nie moze byc do scenario calendar tylko zalezec od obiektu o_gbmscenarios
        gbm_model[:, 0] = self._initialisation_point  # current price
        for t in range(1, len(gbm_model[0])):
            # draw number from normal distribution N(0,sqrt(t*sigma))
            z = np.random.standard_normal(paths_number)
            gbm_model[:, t] = gbm_model[:, t - 1] * np.exp(
                (self._volatility - 0.5 * self._volatility ** 2) * dt[t - 1] +
                self._volatility * np.sqrt(dt[t - 1]) * z)
        return np.transpose(gbm_model)

    def runSimulation(self, simulation_schema: str):
        if simulation_schema == "Euler":
            return self.eulerDiscretisationSchema(simulation_dates=self.scheduled_dates,simulation_grid=self.year_fractions)
        elif simulation_schema=="Milstein":
            return self.milsteinDiscretisationSchema(simulation_dates=self.scheduled_dates,simulation_grid=self.year_fractions)
        elif simulation_schema=="Exact_Solution":
            return self.geometricBrownianMotion(simulation_dates=self.scheduled_dates,simulation_grid=self.year_fractions)
        else:
            raise ValueError("This schema does not exist! Please chose 'Euler', 'Milstein', 'Exact_Solution" )


    def getPathsMetrics(self, df, t_quantiles_name, t_quantiles_values):
        metric_dic = dict()
        for q_name, q_value in zip(t_quantiles_name, t_quantiles_values):
            metric_dic[q_name] = df.quantile(q_value, axis=1)
        metric_dic['mean'] = df.mean(axis=1)
        df_metrics = pd.DataFrame.from_dict(metric_dic, orient='columns')
        df_metrics.index = self.dt_l_dates
        return df_metrics
