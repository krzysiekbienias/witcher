from witcher.python_tool_kit.IOToolKit import XlWingsTools
from witcher.black_scholes_framework.pricing_environment.PricingEnvironment import PricingEnvironment
from witcher.black_scholes_framework.pricing.AnalyticalPrice import EuropeanOptionHandler,MarketEnvironment
from witcher.black_scholes_framework.pricing.AnalyticalPrice import BlackScholesAnalyticalPrice
from witcher.simulation_models.SimulationEnvironment import SimulationEnvironment
from witcher.simulation_models.SimulationModels import GeometricBrownianMotion
from witcher.flask_app import app


from  datetime import datetime
import pandas as pd
import os
from flask import Flask

from flask_restful import Api
from flask_restful import Resource
from http import HTTPStatus


if __name__=="__main__":
    _pricing_module=True
    _simulation_module=False

    # -----------------------
    # Region: Input Output location
    # -----------------------
    io_path=r"/Users/krzysiekbienias/Documents/GitHub/Witcher_In_Finance_world/io"
    if not os.path.isdir(io_path):
            raise ValueError("Path you chosen does not exists!")
    # -----------------------
    # Region: Input Output location
    # -----------------------
    if _pricing_module:
        print("")
        print ("You are running pricing module...")
        pricing_environment = PricingEnvironment(valuation_date="2023-4-22",
                                        termination_date="2023-7-22",
                                        frequency='once',
                                        year_fraction_convention='Actual365',
                                        calendar='USA')
        pricing_environment.displaySchedule()
        print("-.-"*20)
        european_option=EuropeanOptionHandler(option_type="PUT",
                                              option_strike=67)
        print(european_option)
        print("-.-"*20)

        print("-.-"*20)
        market_env=MarketEnvironment(underlier_price=69,
                                    risk_free_rate=0.06,
                                    implied_volatility=0.25)
        print(market_env)
        print("-.-"*20)

        analytical_price=BlackScholesAnalyticalPrice(option=european_option,
                                                    market_env=market_env,
                                                    valuation_date=pricing_environment._str_valuation_date,
                                                    termination_date=pricing_environment._str_termination_date,
                                                    frequency=pricing_environment._s_frequency,
                                                    year_fraction_convention=pricing_environment._s_year_fraction_conv,
                                                    calendar=pricing_environment._s_calendar

                                                    )
        print(f'Option price = {analytical_price.black_scholes_price}')
    
    if _simulation_module:
        print("")
        print ("You are running simulation module...")
        output_name="risk_factors.xlsx"
        XlWingsTools.createNewExcelFile(os.path.join(io_path,output_name))
        XlWingsTools.clearAllSpreadSheet(os.path.join(io_path,output_name))
        print("File for presenting results has been prepared.")
        gbm=GeometricBrownianMotion(start_simulation_date=datetime(2022, 4, 10),
                                    end_simulation_date=datetime(2022, 7, 10),
                                    calendar="USA",
                                    year_fraction_convention="Actual365",
                                    frequency="daily",
                                    drift=0.4,
                                    volatility=0.32,
                                    initialisation_point=44,
                                    simulation_schema="Exact_Solution")
        
