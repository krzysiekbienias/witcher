import pandas as pd
import numpy as np
import os

import xlwings as xw
from typing import Iterable, List, Tuple, Dict, TypeVar

HM=TypeVar("HM",bound=Dict)
T=TypeVar("T")


class PandasTool:

    @staticmethod
    def genericPivotTable(df:pd.DataFrame,
                          pivot_index:List[str],
                          values_:List[str],
                          agg_fun_:HM)->pd.DataFrame:
        """genericPivotTable
        This method creates pivot table from passing data frame

        Parameters
        ----------
        df : pd.DataFrame
            data frame to be pivoted
        pivot_index : List[str]
            index of pivot table
        values_ : List[str]
            columns to be aggregated
        agg_fun_ : HM
            _description_

        Returns
        -------
        pd.DataFrame
            data frame after pivot applied.
        """
        summary_pivot_df=pd.pivot_table(df,values=values_,index=pivot_index,aggfunc=agg_fun_)
        return summary_pivot_df

    @staticmethod
    def queryDataFrame(df:pd.DataFrame,
                       query:str,
                       query_argument:str=None)->pd.DataFrame:
        filtered_df=df.query(query)
        filtered_df.reset_index(drop=True,inplace=True)
        return filtered_df
    
    @staticmethod
    def numpy2DataFrame(arr: np.array, date_index: list) -> pd.DataFrame:
        """function convertNumpyToDataFrame

        Parameters
        ----------
        arr : np.array
            _description_
        date_index : list
            List of datetimes

        Returns
        -------
        pd.DataFrame
        """
        df = pd.DataFrame(arr, index=date_index)
        return df
