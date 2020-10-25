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
emv = 0.78 #emissivity


def main():
    emv_factor = 2 / (2 - emv)
    T_eff = (S_0*(1-albedo)/(4*sb)) ** 0.25 # Absence of atmosphere
    T_s =  T_eff * (emv_factor) ** 0.25
    T_a =  T_s * (2 ** (-0.25))

    # In SI flux units W*m^(-2):
    solar_flux = (1/4) * S_0
    surface_flux = sb * (T_s) ** 4
    greenhouse_flux = emv * sb * T_a ** 4
    planetary_flux = (1 - emv)*sb*T_s**4 + emv*sb*T_a**4

    # Percentages should be roughly 100, 115, 45, 70 as per the wikipedia article
    print(np.array([solar_flux, surface_flux, greenhouse_flux, planetary_flux]) * (100 / solar_flux))
    
    return T_s


if __name__ == "__main__":
   r = main()
   print(r - 273.15)