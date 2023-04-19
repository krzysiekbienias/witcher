import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pylab as plt
from collections.abc import Iterable,Sequence
import os
import xlwings as xw
from typing import TypeVar, Iterable, Tuple, Dict, List, Generic, NewType

class IOTools:
    @staticmethod
    def csv2DataFrame(file_name:str,
                      header:str='infer',
                      use_cols=None,
                      index_col=None,
                      d_type=None,
                      sep=",",
                      names=None)->pd.DataFrame:
        """csv2DataFrame
        This method reads comma separate file into a DataFrame.

        Parameters
        ----------
        file_name : str
            a valid string path
        header : str, optional
            row to use a column names by default 'infer'. If none then data are read without columns.
        use_cols : _type_, optional
            _description_, by default None
        index_col : _type_, optional
            _description_, by default None
        d_type : _type_, optional
            _description_, by default None
        sep : str, optional
            _description_, by default ","
        names : _type_, optional
            _description_, by default None

        Returns
        -------
        pd.DataFrame
            two dimensional data structure with labeled columns and indexes.
        """
        df=pd.read_csv(file_name,usecols=use_cols,index_col=index_col,dtype=d_type,header=header,sep=sep,names=names)
        if header is not None:
            df.columns=[column.strip() for column in df.columns]
            df.columns=[column.replace(" ","_") for column in df.columns]
        return df
        



    @staticmethod
    def save_df_to_csv(df:pd.DataFrame,
                      file_name:str):
       

        df.to_csv(file_name)    


    @staticmethod
    def convertXlsx2Csv(input_path:str,
                        save_path:str,
                        sheet_name="Sheet1"):
        """convertXlsx2Csv
        Description
        -----------
        This method convert xlsx format file into csv. It allows to read data frame much quicker in the future in the code

        Parameters
        ----------
        input_path : str
            xlsx buffer file
        save_path : str
            csv file location file
        sheet_name : str, optional
            tab from xlsx file that is going to be saved as csv, by default "Sheet1"
        """

    @staticmethod
    def saveContentToTxt(location:str,
                        arr:Iterable):
        """saveContentToTxt
        Description
        -----------
        This method allows the user to save content of the list into txt file.

        Parameters
        ----------
        location : str
            Entire path for which we content from container want to drop.
        arr : Iterable
            Container with elements to be paste into file.
        Example
        -------
        >>> IOTools.saveContentToTxt(location=r"/Users/krzysiekbienias/Documents/GitHub/EquityAssetClass/drop_point",
        >>>                            arr=["GC","Citi","UBS"])
            
        """
        with open(location,'w') as fp:
            for rf in arr:
                fp.write("%s\ n" %rf)
        print("File has been saved.")                            
                            

class XlWingsTools:
    @staticmethod
    def createNewExcelFile(save_path:str,
                           sheet_names:List[str]=None):
        """createNewExcelFile
        Description
        -----------
        This method creates excel file with specific tabs.

        Parameters
        ----------
        save_path : str
            _description_
        sheet_names : List[str]
            _description_

        Returns
        -------
        _type_
            _description_
        """
        if os.path.isfile(save_path):

            return xw.Book(save_path)
        else:
            if sheet_names is None:
                app=xw.App(visible=True, add_book=True)
                wb = app.books.add()
                wb.save(save_path)
                print(f"New file {save_path} has been created.")
                return wb
            else:
                app=xw.App(visible=True, add_book=True)
                wb=xw.Book()
                for sheet_name in sheet_names:
                    wb.sheets.add(sheet_name)

                wb.save(save_path)
                print(f"New file {save_path} has been created.")
                return wb


    def clearAllSpreadSheet(file_to_clear:str)->None:
        """clearAllSpreadSheet
        Description
        -----------
        This method removes content from each sheet.

        Parameters
        ----------
        file_to_clear : str
            Name of the file to be cleared.

        Returns
        -------
        None
        """
        wb=xw.Book(file_to_clear)
        workbook_sheets=wb.sheets
        for workbook_sheet in workbook_sheets:
            workbook_sheet.clear()

        


    @staticmethod
    def insertDF(xw_book:xw.Book,
                 df:pd.DataFrame,
                 sheet_name:str="Sheet1",
                 anchor:str="A1",
                 index_flag:bool=True)->None:
        """insertDF
        Description
        -----------


        Parameters
        ----------
        xw_book : xw.Book
            _description_
        df : pd.DataFrame
            _description_
        sheet_name : str, optional
            _description_, by default "Sheet1"
        anchor : str, optional
            _description_, by default "A1"
        index_flag : bool, optional
            _description_, by default True
        """
        if sheet_name in  xw_book.sheet_names:
            xw_sheet= xw_book.sheets[sheet_name]
            xw_sheet.range(anchor).options(pd.DataFrame,
                                        index=index_flag,
                                        expand='table').value=df
        else:
            xw_book.sheets.add(sheet_name)
            xw_sheet.range(anchor).options(pd.DataFrame,
                                        index=index_flag,
                                        expand='table').value=df

        
    @staticmethod
    def insertPlotFromFig(sheet,
                          fig,
                          location:str="A1",
                          name:str="MyPlot",
                          )->None:
        
        sheet.pictures.add(fig,
                           name=name,
                           left=sheet.range(location).left,
                           top=sheet.range(location).top)
        


    @staticmethod
    def insertPlotFromDF(sheet:xw.sheets,
                         ax_obj:plt.axes,
                         anchor:str,
                         title:str=None,
                         height=200,
                         width=300)->None:
        """insertPlotFromDF
        Description
        -----------
        This method drops a plot from DataFrame object in chosen tab and cell. 

        Parameters
        ----------
        sheet : T
            sheet name
        ax_obj : T
            _description_
        anchor : str
            location of graph. It must be in format that corresponds to Excel cell. For instance 'A1'
        title : str, optional
            title of the graph, by default None
        height : int, optional
            width of the graph, by default 200
        width : int, optional
            , by default 300
        """

        fig=ax_obj.get_figure()
        sheet.pictures.add(fig,
                           left=sheet.range(anchor).left,
                           top=sheet.range(anchor).left,
                            height=height,
                            width=width)

    @staticmethod
    def insertHeading(sheet,
                     location:str,
                     text:str,
                     rgb_code=(0,0,39)):
        """insertHeading
        Description
        -----------
        This method insert nice heading for chosen element, graph, table into chosen data frame


        Parameters
        ----------
        sheet : 
            
        location : str
            cell address
        text : str
            string to put
        rgb_code : tuple, optional
            color definition, by default (0,0,39)
        """
        sheet[location].value=text
        sheet[location].font.bold=True
        sheet[location].find.size=24
        sheet[location].font.color=rgb_code

    