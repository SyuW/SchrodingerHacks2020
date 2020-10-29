import numpy as np

'''
Basic model of greenhouse effect assuming Earth and atmosphere behave as ideal black bodies, single atmospheric layer, constant albedo/emissivity,
among other things...
See: http://www.realclimate.org/index.php/archives/2007/04/learning-from-a-simple-model/
     https://en.wikipedia.org/wiki/Idealized_greenhouse_model
     https://en.wikipedia.org/wiki/Greenhouse_gas#Greenhouse_gases
     https://www.acs.org/content/acs/en/climatescience/atmosphericwarming/singlelayermodel.html
'''

# constants
S_c = 1366 #W * m^(-2)
sb = 5.67 * 10 ** (-8)
albedo = 0.3
emv = 0.5 #emissivity
# From wikipedia
greenhouse_contributions = {1: 0.58,
                            2: 0.26,
                            3: 0.09,
                            4: 0.07}


def main():
    emv_factor = 2 / (2 - emv)
    T_eff = (S_c*(1-albedo)/(4*sb)) ** 0.25

    # Follows from Stefan-Boltzmann law, surface temperature T_s should be -17 Celsius and 30 celsius
    # for emv = 0 and 1 respectively
    T_s =  T_eff * (emv_factor) ** 0.25
    T_a =  T_s * (2 ** (-0.25)) # Atmospheric temperature

    # In SI flux units W*m^(-2):
    solar_flux = (1/4) * S_c
    surface_flux = sb * (T_s) ** 4
    greenhouse_flux = emv * sb * T_a ** 4
    planetary_flux = (1 - emv)*sb*T_s**4 + emv*sb*T_a**4

    # Percentages should be roughly 100, 115, 45, 70 as per the wikipedia article for emv =
    print(np.array([solar_flux, surface_flux, greenhouse_flux, planetary_flux]) * (100 / solar_flux))

    return T_s


if __name__ == "__main__":
   r = main()
   print(r - 273.15)
