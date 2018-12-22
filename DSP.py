#coding: utf-8
import math

class DSP():
    def __init__(self,dFreq):
        self.input_data = [] # Локальная переменная для хранения входного массива пустая при объявлении
        self.output_data = [] # Локальная переменная для зранения выходного массива пустая при объявлении
        self.dFreq = dFreq # Частота дискретизации входного массива
        self.h_l = 17 # Длина импульсной характеристики фильтра для свертки
        self.Hlp = [0] * self.h_l # Массив для импульсной характеристики (ИХ) фнч
        self.Hhp = [0] * self.h_l # Массив для ИХ фвч
        self.hFreq = 0 # Частота среза фильтра ВЧ
        self.lFreq = 0 # Частота среза фильтра НЧ
        self.FFT_data = [0] * (self.dFreq / 2)
        self.AKF_data = []
        self.separation_picks = []
        self.average_period = []
        self.RR_distances = []

    def init_lp_filter(self, lFreq):
        self.lFreq = lFreq
        for i in range((self.h_l - 1) / 2):
            self.Hlp[i + (self.h_l - 1) / 2 + 1] = math.sin(6.283 * (i + 1) * self.lFreq / self.dFreq) / (i + 1)
            self.Hlp[(self.h_l - 1) / 2 - 1 - i] = self.Hlp[i + (self.h_l - 1) / 2 + 1]
        self.Hlp[(self.h_l - 1) / 2] = math.sin((6.283 * 0.0000001 * self.lFreq) / self.dFreq) / (0.0000001)
        s = sum(self.Hlp)
        for i in range(len(self.Hlp)):
            self.Hlp[i] /= s
        return True

    def init_hp_filter(self, hFreq):
        self.hFreq = self.dFreq / 2 - hFreq
        for i in range((self.h_l - 1) / 2):
            if i % 2 == 0:
                self.Hhp[i + (self.h_l - 1) / 2 + 1] = 0 - math.sin(6.283 * (i + 1) * self.hFreq / self.dFreq) / (i + 1)
            else:
                self.Hhp[i + (self.h_l - 1) / 2 + 1] = math.sin(6.283 * (i + 1) * self.hFreq / self.dFreq) / (i + 1)
            self.Hhp[(self.h_l - 1) / 2 - 1 - i] = self.Hhp[i + (self.h_l - 1) / 2 + 1]
        self.Hhp[(self.h_l - 1) / 2] = math.sin((6.283 * 0.0000001 * self.hFreq) / self.dFreq) / (0.0000001)
        s = sum(self.Hhp)
        for i in range(len(self.Hhp)):
            self.Hhp[i] /= s
        return True

    def LPF(self, data):
        self.input_data = data
        self.output_data = [0] * (len(self.input_data) + self.h_l)
        for i in range(len(self.input_data)):
            for j in range(self.h_l):
                self.output_data[i + j] = self.output_data[i + j] + self.input_data[i] * self.Hlp[j]
        return self.output_data[(self.h_l) / 2 - 2 : len(self.input_data)+12]

    def HPF(self, data):
        self.input_data = data
        self.output_data = [0] * (len(self.input_data) + self.h_l)
        for i in range(len(self.input_data)):
            for j in range(self.h_l):
                self.output_data[i + j] = self.output_data[i + j] + self.input_data[i] * self.Hhp[j]
        return self.output_data[(self.h_l) / 2 - 2 : len(self.input_data)+12] # выводим данные с поправкой краевого эффекта

    def FFT(self, data=None):
        if data != None:
            self.output_data = data
        rex = [0] * (self.dFreq / 2)
        imx = [0] * (self.dFreq / 2)
        for i in range(1, self.dFreq / 2):
            for j in range(self.dFreq):
                imx[i] = imx[i] - self.output_data[j] * math.sin(2.0 * 3.1415 * i * j / self.dFreq)
                rex[i] = rex[i] + self.output_data[j] * math.cos(2.0 * 3.1415 * i * j / self.dFreq)
            self.FFT_data[i] = math.sqrt(imx[i]**2 + rex[i]**2)
        return self.FFT_data


    def convert_to_Volts(self, bit_rate, v_ref, amp, data=None):
        if data != None:
            self.output_data = data
        k = (v_ref / 2) / amp / 2.0**bit_rate
        for i in range(len(self.output_data)):
            self.output_data[i] *= k
        return self.output_data

    def init_AKF(self):
        self.AKF_data = []
        for j in range(self.dFreq / 10):  # В цикле:
            d = (1.0 - (j ** 2) / 2.0 ** 4) * math.exp(-j * j / 2.0 ** 4 / 2.0)
            self.AKF_data.append(d)
            if j > 0:
                self.AKF_data.insert(0, d)
        return self.AKF_data

    def get_separation_picks(self, data=None):
        if data != None:
            self.output_data = data
        res = [0] * (len(self.output_data) + len(self.AKF_data))

        temp_top = []
        #temp_bottom = []

        for i in range(len(self.output_data)):
            for j in range(len(self.AKF_data) - 1):
                res[i + j] = res[i + j] + self.output_data[i] * self.AKF_data[j]
        res = res[len(self.AKF_data) / 2: len(self.output_data) + len(self.AKF_data) / 2]
        middle_top = max(res) / 2
        #middle_bottom = min(res) / 2

        for i in range(len(res)):
            if res[i] >= middle_top:
                temp_top.append(res[i])
            else:
                temp_top.append(0)

            #if res[i] <= middle_bottom:
            #    temp_bottom.append(res[i])
            #else:
            #    temp_bottom.append(0)
        self.separation_picks = []
        for i in range(1, len(temp_top) - 1):
            if temp_top[i - 1] < temp_top[i] > temp_top[i + 1]:
                self.separation_picks.append(i)
            #if temp_bottom[i - 1] > temp_bottom[i] < temp_bottom[i + 1]:
             #   Bottom_picks.append(i)

        return self.separation_picks#, len(Bottom_picks)

    def get_average_period(self, data, separations=[]):
        self.separation_picks = separations
        max_period_len = 0
        if data != None:
            self.output_data = data
        max_period_len = 1000
        print len(self.separation_picks)

        self.average_period = [0] * (max_period_len)
        average_center = (len(self.average_period)) / 2

        for i in range(1, len(self.separation_picks) - 1):
            pos = self.separation_picks[i]
            while pos > self.separation_picks[i-1]:
                self.average_period[average_center - (self.separation_picks[i] - pos)] += self.output_data[pos]\
                                                                                          / len(self.separation_picks)
                pos -= 1
            pos = self.separation_picks[i]+1
            while pos < self.separation_picks[i+1]:
                self.average_period[average_center + (pos - self.separation_picks[i])] += self.output_data[pos]\
                                                                                          / len(self.separation_picks)
                pos += 1
        return self.average_period[300:max_period_len-300]

    def get_RR_distances(self, picks=[]):
        if picks != []:
            self.separation_picks = picks
        for i in range(len(self.separation_picks) - 1):
            self.RR_distances.append(self.separation_picks[i+1] - self.separation_picks[i])

        return self.RR_distances