# -*- coding: utf-8 -*- 

'''
Author: ByronVon
Email: wangy@craiditx.com
Version: 
Date: 2020-11-17 18:29:52
LastEditTime: 2020-11-17 23:00:56
'''
import os
import numpy as np
import pandas as pd

class Chunksize(object):

    def __init__(self, path):

        self.path = path ## 存放文件的上上级路径，./base/i/i_1_1_connect123.csv

    def clean(self, list_A, list_B):
        '''
        description: 
        param {*}
        return {*}
        '''
        X, Y = [list_A[0]], [list_B[0]]
        
        for i in range(1,len(list_A)):
            if i > 0:
                if list_A[i] != list_A[i-1] and list_B[i] != list_B[i-1]:
                    X.append(list_A[i])
                    Y.append(list_B[i])
        return X,Y
        
    def divide_angle(self, list_A, list_B):
        X_1, X_2, Y_1, Y_2 = [], [], [], []
        for i in range(1,len(list_A)):
            M= list_A[i]**2 + list_B[i]**2
            if M < 0.067:
                X_1.append(list_A[i])
                Y_1.append(list_B[i])
            if M > 0.067:
                X_2.append(list_A[i])
                Y_2.append(list_B[i])
        return X_1, Y_1, X_2, Y_2

    def divide_area(self, list_A, list_B):
        '''
        description: 分割区间
        param {*}
        return {*}
        '''
        re0, re1, re2, re3 = [], [], [], []

        for i in range(1, len(list_A)) :
            ## 0
            if list_A[i] > 0 and list_B[i] > 0 and abs(list_A[i]) > abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re0.append(np.degrees(inv))
            ## 1
            if list_A[i] > 0 and list_B[i] > 0 and abs(list_A[i]) < abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re1.append(np.degrees(inv))
            ## 1
            if list_A[i] < 0 and list_B[i] > 0 and abs(list_A[i]) < abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re1.append(np.degrees(inv))
            ## 2
            if list_A[i] < 0 and list_B[i] > 0 and abs(list_A[i]) > abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re2.append(np.degrees(inv))
            ## 2
            if list_A[i] < 0 and list_B[i] < 0 and abs(list_A[i]) > abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re2.append(np.degrees(inv))
            ## 3
            if list_A[i] < 0 and list_B[i] < 0 and abs(list_A[i]) < abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re3.append(np.degrees(inv))
            ## 3
            if list_A[i] > 0 and list_B[i] < 0 and abs(list_A[i]) < abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re3.append(np.degrees(inv))
            ## 0
            if list_A[i] > 0 and list_B[i] < 0 and abs(list_A[i]) > abs(list_B[i]):
                inv = np.sqrt(list_A[i]**2+list_B[i]**2)
                re0.append(np.degrees(inv))
        return re0, re1, re2, re3

    def run(self):
        '''
        description: 遍历指定文件夹下的路径并处理
        param {*}
        return {*}
        '''
        ## 依次遍历子文件夹
        res_left, res_right = dict(), dict()
        for folder in os.listdir(self.path):
            path_ = os.path.join(self.path, folder)
            ## 依次遍历子文件夹中的文件
            # left, right = [], []
            for file in os.listdir(path_):
                key = '_'.join(file.split('_')[1:3]) ## 使用'_'连接标签名
                # print(key)
                df = pd.read_csv(os.path.join(path_, file)).reset_index()
                # time_stamp = df['time_stamp']
                gaze_left, gaze_left_ = df['gaze_left_1'], df['gaze_left_2']
                gaze_right, gaze_right_ = df['gaze_right_1'], df['gaze_right_2']
                clean_left = self.clean(gaze_left, gaze_left_)
                clean_right = self.clean(gaze_right, gaze_right_)
                divide_left = self.divide_angle(clean_left[0], clean_left[1]) ## re0, re1, re2, re3
                divide_right = self.divide_angle(clean_right[0], clean_right[1])
                ## re0, re1 处理前2个值
                divide_left_prev = self.divide_area(divide_left[0], divide_left[1])
                divide_right_prev = self.divide_area(divide_right[0], divide_right[1])
                ## re2, re3 处理后两个值
                divide_left_next = self.divide_area(divide_left[2], divide_left[3])
                divide_right_next = self.divide_area(divide_right[2], divide_right[3])
                # left.append([len(i) for i in divide_left_prev + divide_left_next])
                # right.append([len(i) for i in divide_right_prev + divide_right_next])
                ## 将相同tag的文件存入字典的相同字段中
                if key not in res_left:
                    res_left[key] = [[len(i) for i in divide_left_prev+divide_left_next]]
                else:
                    res_left[key].append([len(i) for i in divide_left_prev+divide_left_next])
                if key not in res_right:
                    res_right[key] = [[len(i) for i in divide_right_prev+divide_right_next]]
                else:
                    res_right[key].append([len(i) for i in divide_right_prev+divide_right_next])
                # res_left.append([len(i) for i in divide_left_prev+divide_left_next])
                # res_right.append([len(i) for i in divide_right_prev+divide_left_next])
        return res_left, res_right


if __name__ == "__main__":
    ck = Chunksize(path='./dataset/text')
    res, res_ = ck.run()
    print(res)
    print(res_)