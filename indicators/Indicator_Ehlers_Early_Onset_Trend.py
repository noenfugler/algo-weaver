from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan
from math import isinf

class Indicator_Ehlers_Early_Onset_Trend(Indicator):
    def __init__(self):
        self.min_warmup_candles = 5

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', destinations=['eoti_quotient1', 'eoti_quotient2'], lp_period=30, k1=0.85, k2=0.4):
        # // Highpass filter cyclic components
        # // whose periods are shorter than
        # // 100 bars
        alpha1 = (cos(.707 * 2*pi / 100) + sin(.707 * 2*pi / 100) - 1) / cos(.707 * 2*pi / 100)
        data['_hp'] = 0.0
        data['_filt'] = 0.0
        data['_peak'] = 0.0
        data['0'] = 0.0
        self.set_up_super_smoother_parameters(ss_period=lp_period)
        for row_num in range(2,len(data)):
            data.at[row_num,'_hp']=(1-alpha1/2)**2 *  (data.loc[row_num,source] - 2*data.loc[row_num-1,source] + data.loc[row_num-2, source]) \
                              + 2*(1-alpha1) * data.loc[row_num-1,'_hp'] - (1-alpha1)**2*data.loc[row_num-2,'_hp']
            # HP                     = (1 - alpha1 / 2) * (1 - alpha1 / 2) * (Close - 2 * Close[1] + Close[2])
            #                     + 2 * (1 - alpha1) * HP[1]                - (1 - alpha1) * (1 - alpha1) * HP[2];
            # // SuperSmoother Filter
            data.at[row_num,'_filt']        = self.ss_c1 * (data.loc[row_num,'_hp']   + data.loc[row_num - 1, '_hp'] ) / 2 \
                                            + self.ss_c2 * data.loc[row_num - 1, '_filt']     + self.ss_c3 * data.loc[row_num-2,'_filt']
            # data.at[row_num, destination]   = self.ss_c1 * (data.loc[row_num, source] + data.loc[row_num - 1, source]) / 2 \
            #                                 + self.ss_c2 * data.loc[row_num - 1, destination] + self.ss_c3 * data.loc[row_num - 2, destination];

            # Filt = c1 * (HP + HP[1]) / 2 + c2 * Filt[1] + c3 * Filt[2];
            #Fast attack - slow decay algorithm
            data.at[row_num,'_peak']=0.991*data.loc[row_num-1,'_peak']
            # Peak = .991 * Peak[1];
            # If AbsValue(Filt) > Peak then Peak = AbsValue(Filt);
            if abs(data.loc[row_num,'_filt']) > data.loc[row_num,'_peak']:
                data.at[row_num,'_peak']=abs(data.loc[row_num,'_filt'])
            # Normalised Roofing Filter
            if data.loc[row_num,'_peak']!=0:
                data.at[row_num,'_x']=data.loc[row_num,'_filt']/data.loc[row_num,'_peak']
            # if Peak <> 0 then
            #     X = Filt / Peak;
            data.at[row_num,destinations[0]]=(data.loc[row_num,'_x']+k1)/(k1*data.loc[row_num,'_x']+1)
            data.at[row_num,destinations[1]]=(data.loc[row_num,'_x']+k2)/(k2*data.loc[row_num,'_x']+1)
            # Quotient1 = (X + K1) / (K1 * X + 1);
            # Quotient2 = (X + K2) / (K2 * X + 1);

