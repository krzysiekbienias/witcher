# Witcher library

The package aim is to provide a comprehensive set of tools to help in different aspect of pricing plain vanilla european options in Black Scholes framework. Additional module provides that provides also extra module for sensitivity analysis. 

#### Table of contents
[Instalation](#Instalation)  
[Project Structure](#ProjectStructure)  
[General Overview](#GeneralOverview)  
[Configuration](#Configuration)  
[Underlier Simulation](#UnderlierSimulation)  
[Black-Scholes Pricing Framework](#BlackScholesPricingFramework)  
[Sensitivity Analysis](#SensitivityAnalysis)  
[Utils](#Utils)  

## Instalation
To use the package you need to clone the repository first. The package itself has a numerous dependencies and it is better to isolate environment for this module. To run it properly ple

## Dependecies
To run the code smoothly a User must first import QuantLib library. From QuantLib we laverage only calendar schedule and lifecycle of trades. All analytical formula are implemented from scratch.

## Documentation
Detailed documentation might be find under following location:
https://raw.githack.com/krzysiekbienias/witcher/master/docs/build/html/py-modindex.html

https://raw.githack.com/krzysiekbienias/witcher/master/docs/build/html/index.html

## Structure
```
Witcher Project
--dev_docs
--io
--src
   |--witcher
         |--black_scholes_framework
                |--pricing_environment
                |--pricing    

    |
    |--market_environment
    |--pricing_environment
    |--pricing
          
    |--sensitivity_analysis
    |--simulation_models
    |--tool_kit
    |--utils
--python_tool_kit
--jupyter_lab

    

```



