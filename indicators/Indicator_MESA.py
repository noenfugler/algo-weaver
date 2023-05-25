#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

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