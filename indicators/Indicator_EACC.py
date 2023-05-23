#Ehlers Adaptive Cyber Cycle Indicator

from indicators.Indicator_class import Indicator

import math

class Indicator_EACC(Indicator):
    def __init__(self):
        self.min_warmup_candles=25

    def create(self, source='price', alpha=0.07):
        self.df['cyber_cycle']=0.0
        self.df['acc_presmooth']=0.0
        self.df['adaptive_cyber_cycle']=0.0
        self.df['acc_q1']=0.0
        self.df['acc_I1']=0.0
        self.df['acc_deltaphase']=0.0
        self.df['acc_median_delta']=0.0
        self.df['acc_dc']=0.0
        self.df['acc_inst_period']=0.0
        self.df['acc_period']=0.0
        self.df['acc_trigger']=0.0

        for row_num in range(3,8):
            self.df.at[row_num,'cyber_cycle'] = (self.df.loc[row_num,source] - 2*self.df.loc[row_num-1,source] + self.df.loc[row_num-2,source])/4
            self.df.at[row_num,'acc_presmooth']=(self.df.loc[row_num,source] + 2*self.df.loc[row_num-1,source] + 2*self.df.loc[row_num-2,source] + self.df.loc[row_num-3,source])/6  #10
            self.df.at[row_num,'adaptive_cyber_cycle'] = (self.df.loc[row_num,source] - 2*self.df.loc[row_num-1,source] + self.df.loc[row_num-2,source])/4

        for row_num in range(8,len(self.df)):
            self.df.at[row_num,'acc_presmooth']=(self.df.loc[row_num,source] + 2*self.df.loc[row_num-1,source] + 2*self.df.loc[row_num-2,source] + self.df.loc[row_num-3,source])/6  #10
            self.df.at[row_num,'cyber_cycle']=((1-0.5*alpha)**2) * (self.df.loc[row_num,'acc_presmooth'] - 2*self.df.loc[row_num-1,'acc_presmooth'] + self.df.loc[row_num-2,'acc_presmooth']) \
                    + 2*(1 - alpha) * self.df.loc[row_num-1,'cyber_cycle'] - ((1 - alpha)**2)*self.df.loc[row_num-2,'cyber_cycle']
            self.df.at[row_num,'acc_q1']=(0.962*self.df.loc[row_num,'cyber_cycle'] + 0.5769*self.df.loc[row_num-2,'cyber_cycle']-0.5769*self.df.loc[row_num-4,'cyber_cycle']-0.962*self.df.loc[row_num-6,'cyber_cycle'])*(0.5*0.8*self.df.loc[row_num-1,'acc_inst_period'])   #12
            self.df.at[row_num,'acc_I1']=self.df.loc[row_num-3,'acc_q1'] #13
            if self.df.loc[row_num,'acc_q1'] != 0 and self.df.loc[row_num-1,'acc_q1'] != 0:
                self.df.at[row_num,'acc_deltaphase'] = (self.df.loc[row_num,'acc_I1']/self.df.loc[row_num,'acc_q1']-self.df.loc[row_num-1,'acc_I1']/self.df.loc[row_num-1,'acc_q1']) \
                        / (1 + self.df.loc[row_num,'acc_I1'] * self.df.loc[row_num-1,'acc_I1'] / (self.df.loc[row_num,'acc_q1'] * self.df.loc[row_num-1,'acc_q1']))
            if self.df.loc[row_num,'acc_deltaphase'] < 0.1:
                self.df.at[row_num, 'acc_deltaphase'] = 0.1
            if self.df.loc[row_num,'acc_deltaphase'] > 1.1:
                self.df.at[row_num, 'acc_deltaphase'] = 1.1
            self.df.at[row_num,'acc_median_delta'] = self.df.loc[row_num-4:row_num,'acc_deltaphase'].median()
            if self.df.loc[row_num,'acc_median_delta'] ==0 :
                self.df.at[row_num,'acc_dc'] = 0.0
            else:
                self.df.at[row_num, 'acc_dc'] = 2 * 3.14159 / self.df.loc[row_num,'acc_median_delta'] + 0.5
            self.df.at[row_num, 'acc_inst_period'] = (self.df.at[row_num, 'acc_dc'] + 2 * self.df.at[row_num - 1, 'acc_inst_period']) / 3
            self.df.at[row_num, 'acc_period'] = 0.15 * self.df.at[row_num, 'acc_inst_period'] + 0.85 * self.df.at[row_num - 1, 'acc_period']
            alpha1 = 2 / (self.df.at[row_num, 'acc_period'] + 1)
            self.df.at[row_num,'adaptive_cyber_cycle']=((1-0.5*alpha1)**2) * (self.df.loc[row_num,'acc_presmooth'] - 2*self.df.loc[row_num-1,'acc_presmooth'] + self.df.loc[row_num-2,'acc_presmooth']) \
                    + 2*(1 - alpha1) * self.df.loc[row_num-1,'adaptive_cyber_cycle'] - ((1 - alpha1)**2)*self.df.loc[row_num-2,'adaptive_cyber_cycle']

        self.df['acc_trigger']=self.df['adaptive_cyber_cycle'].shift(1)
        self.df['acc_momentum']=2*self.df['adaptive_cyber_cycle']-self.df['adaptive_cyber_cycle'].shift(1)
        self.df['acc_average']=(self.df['adaptive_cyber_cycle']+self.df['acc_momentum'])/2

