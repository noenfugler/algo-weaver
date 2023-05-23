from indicators.Indicator_class import Indicator

# import math
from memspectrum import MESA

class Indicator_MESA(Indicator):
    def create(self, source='close', alpha=0.07):
        M = MESA()
        # Computation of the spectrum on sampling frequencies
        data = self.df.loc[-20:, source]
        P, a_k, opt = M.solve(data)
        spectrum, frequencies = M.spectrum(data)
        pass

        fig = plt.figure(1)
        ax  = fig.add_subplot(111)
        # ax.loglog(f[:N//2], PSD[:N//2],'-k')
        ax.set_xlim(1e-5,srate/2.)
        ax.set_xlabel("frequency (1/months)")
        ax.set_ylabel("PSD (months)")
        plt.show()