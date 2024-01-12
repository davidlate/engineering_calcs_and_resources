import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI


class Convert:
    def C_to_K(Celcius):
        K = Celcius + 273.15
        return K

    def F_to_K(Farenheit):
        K = (Farenheit - 32) * 5/9 + 273.15
        return K

    def C_to_F(Celcius):
        F = Celcius * 9/5 + 32
        return F

    def psia_to_Pa(psia):
        Pa = psia * 6894.7572931783
        return Pa

class Calc:

    def findRhoCoolProp_kg_m3(temp_K, press_Pa, fluid):
        rho = PropsSI('D', 'T',temp_K, 'P',press_Pa,fluid)
        return rho

    def findRhoIdealGasLaw(temp_K, press_Pa, R= 296.80):  #Default is Nitrogen
        rho = press_Pa / (temp_K * R)
        return rho

    def findIdealGasDensityErrPercent(temp_K, press_Pa, fluid='Nitrogen', R= 296.80):
        rho_CoolProp = Calc.findRhoCoolProp_kg_m3(temp_K, press_Pa, fluid)
        
        rho_Ideal = Calc.findRhoIdealGasLaw(temp_K, press_Pa, R)

        rhoErrPercent = ( (rho_Ideal - rho_CoolProp) / rho_CoolProp ) * 100

        return rhoErrPercent


class Plotting: 

    def plotIdealGasErrPercent(fluid, R):

        T_F      = np.arange(-40, 122, 2)
        P_psia   = np.arange(1, 6025, 25)

        T_K = Convert.F_to_K(T_F)
        P_Pa = Convert.psia_to_Pa(P_psia)

        T_F, P_psia = np.meshgrid(T_F, P_psia)
        T_K, P_Pa = np.meshgrid(T_K, P_Pa)

        DensErrPerc = np.vectorize(Calc.findIdealGasDensityErrPercent)

        levels = np.arange(-12.5, 30, 2.5)
        levels = np.append(levels, [-1, 1])
        levels = np.sort(levels)

        fig, ax = plt.subplots()
        cs = plt.contourf(P_psia, T_F, DensErrPerc(temp_K=T_K, press_Pa = P_Pa, fluid = fluid, R = R), levels=levels)
        cd = plt.contour(P_psia, T_F, DensErrPerc(temp_K=T_K, press_Pa = P_Pa, fluid = fluid, R = R), colors='black', levels=levels, linestyles = ':')
        xticks = np.arange(0, 6500, 500)
        yticks = np.arange(-40, 130, 10)
        ax.clabel(cd, inline = True, fontsize = 10, colors = 'k', fmt='%1.1f%%')
        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        fig.set_size_inches(8,6)
        #fig.colorbar()
        plt.suptitle("{:} Density, Ideal Gas Law vs CoolProp".format(fluid), fontsize=11)
        plt.title(r'Value shown: $\frac{\rho_{IdealGasLaw}-\rho_{CoolProp}}{\rho_{CoolProp}}$ * 100%', fontsize=9)
        plt.xticks(rotation=60)
        plt.xlabel("Pressure [PSIA]")
        plt.ylabel("Temperature [°F]")
        plt.grid(True, linestyle=":")
        cbar = plt.colorbar(cs, format='%1.1f%%')
        fig.savefig("DensityErrCalc.pdf")
        plt.show()

if __name__ == '__main__':

    fluid = "Nitrogen"
    R = 296.80
    Plotting.plotIdealGasErrPercent(fluid=fluid, R=R)