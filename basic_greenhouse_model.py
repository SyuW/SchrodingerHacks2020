import numpy as np
'''
Basic model of greenhouse effect assuming Earth and Sun both behave as ideal black bodies, single atmospheric layer, constant albedo/emissivity, 
among other things...
See: http://www.realclimate.org/index.php/archives/2007/04/learning-from-a-simple-model/
     https://en.wikipedia.org/wiki/Idealized_greenhouse_model

Extensions for introducing realism/complexity:
- feedback mechanisms for albedo and atmospheric emissivity
- Atmospheric convection
- Clouds (aggregations of water droplets in sky)
- Multi-layer representation of atmosphere
'''

# constants
S_0 = 1366 #W * m^(-2)
sb = 5.67 * 10 ** (-8)
albedo = 0.3
emv = 1 #emissivity


def main():
    emv_factor = 2 / (2 - emv)
    T_eff = (S_0*(1-albedo)/(4*sb)) ** 0.25 # Absence of atmos.
    T_s =  T_eff * (emv_factor) ** 0.25
    return T_s


if __name__ == "__main__":
   r = main()
   print(r - 273.15)