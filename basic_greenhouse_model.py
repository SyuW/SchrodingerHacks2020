import numpy as np


# constants
S_0 = 1366 #W * m^(-2)
sb = 5.67 * 10 ** (-8)
albedo = 0.3
emv = 1 #emissivity


def main():
    #print((S_0*(1-albedo)/(4*sb))**(1/4))
    T_eff = (S_0*(1-albedo)/(4*sb)) ** 0.25 # Absence of atmos.
    emv_factor = 2 / (2 - emv)
    T_s =  T_eff * (emv_factor) ** (0.25)
    return T_s


if __name__ == "__main__":
   r = main()
   print(r - 273.15)