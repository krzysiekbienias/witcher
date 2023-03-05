
import QuantLib as ql
from typing import TypeVar,Iterable,Tuple,Dict,List,Generic,NewType
from datetime import datetime


QL=NewType("QL",ql)
DT=TypeVar('DT',bound=datetime)
HM=TypeVar("HM",bound=Dict)

class QuantLibToolKit:

    _weekday_corrections={"Following":ql.Following,
                         "ModifiedFollowing":ql.ModifiedFollowing,
                         "Preceding":ql.ModifiedPreceding,
                         "ModifiedPreceding":ql.ModifiedPreceding,
                         "Unadjusted":ql.Unadjusted

                         }

    _date_generation_rules={"Backward":ql.DateGeneration.Backward,
                      "Forward":ql.DateGeneration.Forward}

    @staticmethod
    def convertDate2QlDate(date:DT)->QL:
        """convertDate2QlDate
        Description
        -----------
        function converts datetime date object and convert to equivalent quantlib Object

        Parameters
        ----------
        date : DT
            date time object that gonna be converted. Must be passed as year, month, day

        Returns
        -------
        QL
            date as a QuantLib object
        """


        ql_date = ql.Date(date.day, date.month, date.year)
        return ql_date


    @staticmethod
    def setCalendar(country:str="theUK")->QL:
        """setCalendar
        Description
        -----------

        Parameters
        ----------
        country : str
            Name of country according to business operates. Currently following calendars are available:
            - USA
            - UK
            - Switzerland
            - Poland

        Returns
        -------
        QL
            _description_
        """
        if country not in ("USA", "theUK", "Switzerland", "Poland"):
            raise ValueError("calendar name must be one of the following: 'USA', 'theUK', 'Switzerland', 'Poland'")
        if country == 'USA':
            return ql.UnitedStates(ql.UnitedStates.NYSE)
        if country == 'theUK':
            return ql.UnitedKingdom()
        if country == 'Switzerland':
            return ql.Switzerland()
        if country == 'Poland':
            return ql.Poland()

    @staticmethod
    def setDateCorrectionsSchema(corrections_map:HM=_weekday_corrections,
                              correction_rule:str="Following")->int:
        """setBusinessConvention
        Description
        -----------
        This method defines business convention.

        Returns
        -------
        _type_
            _description_
        """
        return corrections_map[correction_rule]

    @staticmethod
    def setRuleOfDateGeneration(_date_generation_rules=_date_generation_rules)->int:
        """setRuleOfDateGeneration
        Description
        -----------

        Returns
        -------
        _type_
            _description_
        """
        return ql.DateGeneration.Forward


    @staticmethod
    def defineSchedule(effective_day:DT,
                       termination_date:DT,
                       freq_period_:str="monthly",
                       calendar_:str="theUK")->QL:
        """defineSchedule
        Description
        -----------


        Parameters
        ----------
        effective_day : DT
            _description_
        termination_date : DT
            _description_
        freq_period_ : str, optional
            _description_, by default "monthly"
        calendar_ : str, optional
            _description_, by default "theUK"

        Returns
        -------
        QL
            _description_
        """

        return ql.MakeSchedule(effectiveDate=QuantLibToolKit.convertDate2QlDate(effective_day),
                        terminationDate=QuantLibToolKit.convertDate2QlDate(termination_date),
                        frequency=QuantLibToolKit.setFrequency(freq_period_),
                        calendar=QuantLibToolKit.setCalendar(calendar_))

    @staticmethod
    def setFrequency(freq_period:str)->int:
        """setFrequency
        Description
        -----------
        This function set frequency period for calendar schedule.

        Parameters
        ----------
        freq_period : str
            one of possible frequency period.

        Returns
        -------
        QL
            frequency Period
        """
        if freq_period not in ('daily', "once", "monthly", "quarterly","annual", "semiannual"):
            raise ValueError(" Name of the period must be one of following 'daily', 'once','monthly','quarterly','annual','semiannual'. ")


        if freq_period=='daily':
            return ql.Daily
        if freq_period=='once':
            return ql.Once
        if freq_period=='monthly':
            return ql.Monthly
        if freq_period=='quarterly':
            return ql.Quarterly
        if freq_period=='annual':
            return ql.Annual
        if freq_period=='semiannual':
            return ql.Semiannual

