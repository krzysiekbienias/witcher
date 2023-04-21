
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
    def string_2qlDate(date:str)->QL:
        """string_2qlDate
        Description
        -----------
        function converts string date representation and convert to equivalent quantlib object.
        Date must be in form Y-m-d.
        Parameters
        ----------
        date : str
            date time object that gonna be converted. Must be passed as year, month, day

        Returns
        -------
        QL
            date as a QuantLib object
        """

        dt_date=datetime.strptime(date,"%Y-%m-%d")
        ql_date = ql.Date(dt_date.day, dt_date.month, dt_date.year)
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
    def defineSchedule(effective_day:str,
                       termination_date:str,
                       freq_period:str="monthly",
                       calendar:str="theUK")->ql.Schedule:
        """defineSchedule
        Description
        -----------
        Simpler version of defining schedule object. Only required parameters
        
        Parameters
        ----------
        effective_day : str
            _description_
        termination_date : str
            _description_
        freq_period : str, optional
            _description_, by default "monthly"
        calendar : str, optional
            _description_, by default "theUK"

        Returns
        -------
        ql.Schedule
            _description_
        """

        return ql.MakeSchedule(effectiveDate=QuantLibToolKit.string_2qlDate(effective_day),
                        terminationDate=QuantLibToolKit.string_2qlDate(termination_date),
                        frequency=QuantLibToolKit.setFrequency(freq_period),
                        calendar=QuantLibToolKit.setCalendar(calendar))

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

