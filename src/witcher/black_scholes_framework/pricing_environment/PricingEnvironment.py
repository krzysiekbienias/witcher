import QuantLib as ql
from datetime import datetime
import os
import pandas as pd
from typing import TypeVar, Iterable, Tuple, Dict, List, Generic, NewType

from witcher.python_tool_kit.QuantLibToolKit import QuantLibToolKit



QL = NewType("QL", ql)

DT = TypeVar('DT')


class PricingEnvironment():

    def __init__(self,
                 valuation_date: str,
                 termination_date: str,
                 calendar: str = "theUK",
                 year_fraction_convention: str = "Actual365",
                 frequency: str = "Monthly",
                 **kwargs):
        """
        Description
        -----------
        This class sets up generic the environment for pricing different financial instruments.

        Parameters
        ----------
        valuation_date : str
            The date you want to price financial instrument. Format Y-m-d.

        termination_date : str
            Date after which your trade expires. Format Y-m-d.
        calendar : str, optional
            Name of the specific calendar of dates to follow, by default "theUK". It corresponds with name of country.
        Possible calendar to chose:
        - theUk
        - USA
        - Poland
        - Switzerland
        year_fraction_convention : str, optional
            Name of year count convention that sets rule how year fraction to be calculated, by default "Actual365"
            Another possible:
            - Actual360, 
            - Actual365,
            - ActualActual,
            - Thirty360
            - Business252 
        frequency : str, optional
            Name of frequency according to with tenors are generated. In particular daily if we want to have business days in our schedule,
              by default "monthly"
            Possible parameters:
            - daily
            - once
            - monthly
            - quarterly
            - annual
            - semiannual


        Note
        ----
        Please note that within this class as well as QuantLibToolKid are defined different static methods where variable are converted into.
        This interface allows to User do not take care about it.

        """

        # -----------------------
        # Region: Initialization
        # -----------------------
        self._str_valuation_date = valuation_date
        self._str_termination_date = termination_date
        self._s_calendar = calendar
        self._s_year_fraction_conv = year_fraction_convention
        self._s_frequency = frequency
        # -----------------------
        # END Region: Initialization
        # -----------------------

        # -----------------------
        # Region: QuantLib Converter
        # -----------------------
        ql_valuation_date = QuantLibToolKit.string_2qlDate(
            date=self._str_valuation_date)
        ql_termination_date = QuantLibToolKit.string_2qlDate(
            date=self._str_termination_date)
        date_correction_schema = QuantLibToolKit.set_date_corrections_schema()
        ql_year_fraction_conv = self.set_year_fraction_convention(
            year_fraction_conv=self._s_year_fraction_conv)
        ql_calendar = QuantLibToolKit.set_calendar(country=self._s_calendar)

        ql_schedule = self.set_schedule(effectiveDate=ql_valuation_date,
                                       terminationDate=ql_termination_date,
                                       tenor=ql.Period(QuantLibToolKit.set_frequency(
                                           freq_period=self._s_frequency)),
                                       calendar=ql_calendar)
        # -----------------------
        # Region: QuantLib Converter
        # -----------------------

        # -----------------------
        # Region: Attributes
        # -----------------------
        self.scheduled_dates = list(ql_schedule)
        self.year_fractions = self.get_year_fraction_sequence(schedule=ql_schedule,
                                                           convention=ql_year_fraction_conv)
        self.days_until_expiration=self.scheduled_dates[-1]-self.scheduled_dates[0]
        # -----------------------
        # End Region: Attributes
        # -----------------------

    def set_year_fraction_convention(self, year_fraction_conv: str = "Actual365") -> QL:
        """set_year_fraction_convention
        Description
        -----------
        Function defines how we will calculate year fraction.

        Parameters
        ----------
        year_fraction_conv : string
             Available alternatives: Actual360, Actual365, ActualActual, Thirty360, Business252


        Returns
        -------
        ql.FractionConvention

        """
        if (year_fraction_conv == 'Actual360'):
            day_count = ql.Actual360()
            return day_count
        elif (year_fraction_conv == 'Actual365'):
            day_count = ql.Actual365Fixed()
            return day_count
        elif (year_fraction_conv == 'ActualActual'):
            day_count = ql.ActualActual()
            return day_count
        elif (year_fraction_conv == 'Thirty360'):
            day_count = ql.Thirty360()
            return day_count
        elif (year_fraction_conv == 'Business252'):
            day_count = ql.Business252()
            return day_count


    def set_schedule(self,
                    effectiveDate: ql.Date,
                    terminationDate: ql.Date,
                    tenor: ql.Period,
                    calendar: ql.Calendar,
                    convention=QuantLibToolKit.set_date_corrections_schema(),
                    termination_date_convention=QuantLibToolKit.set_date_corrections_schema(),
                    rule: ql.DateGeneration = QuantLibToolKit.set_rule_of_date_generation(date_generation_rules="forward"),
                    endOfMonth: bool = False) -> ql.Schedule:
        """set_schedule
        Description
        -----------
        Method creates the schedule that handle with life cycle of a trade. The heart of the class.

        Parameters
        ----------
        effectiveDate : ql.Date
            _description_
        terminationDate : ql.Date
            _description_
        tenor : ql.Period
            _description_
        calendar : ql.Calendar
            _description_
        convention : _type_, optional
            _description_, by default QuantLibToolKit.set_date_corrections_schema()
        termination_date_convention : _type_, optional
            _description_, by default QuantLibToolKit.set_date_corrections_schema()
        rule : ql.DateGeneration, optional
            _description_, by default QuantLibToolKit.setRuleOfDateGeneration()
        endOfMonth : bool, optional
            _description_, by default False

        Returns
        -------
        ql.Schedule
            _description_
        """

        return ql.Schedule(effectiveDate, terminationDate, tenor, calendar, convention, termination_date_convention, rule, endOfMonth)

    def get_year_fraction_sequence(self,
                                schedule: ql.Schedule,
                                convention: QL) -> List[float]:
        """consecutiveDatesYearFraction
        Description
        -----------
        For given sequence of dates returns arr of list year fractions with edges T_i-1 and T_i


        Returns
        -------
        List[float]
            list of year fraction's
        """
        lf_year_fraction = []
        scheduled_dates = list(schedule)
        if len(scheduled_dates) == 2:
            # frequency probably set as 'once' so only valuation and termination date has been provided
            return convention.yearFraction(scheduled_dates[0], scheduled_dates[1])
        for i in range(1, len(scheduled_dates)):
            temp_yf = convention.yearFraction(
                scheduled_dates[i-1], scheduled_dates[i])
            lf_year_fraction.append(temp_yf)
        return lf_year_fraction

    def display_schedule(self) -> None:
        """display_schedule
        Description
        -----------
        This method display information about schedule.
        """

        dates = self.scheduled_dates
        if len(dates) == 2:
            print("At valuation date there is still {0:.2f} of the year.".format(
                self.year_fractions))
        else:
            year_fractions = [None]+self.year_fractions
            df_schedule = pd.DataFrame(zip(dates, year_fractions), columns=[
                                       'Calendar_Grid', "Year_Fraction"])
            print(df_schedule)
