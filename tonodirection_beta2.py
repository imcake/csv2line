#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-12
# @Author  : imcake (imc4k3@gmail.com)
# @Link    : https://github.com/imcake


import os
import csv
import pandas as pd

######################################################
# 需要修改部分
# hasdirection --> 有向的文件名（不含扩展名）
# from_header --> 有向流起点列名
# to_header --> 有向流终点列名
# vol_header --> 有向流流量列名
######################################################
hasdirection = 'from_to_dy_jz_latlon'
from_header = 'from_id'
to_header = 'to_id'
vol_header = 'total'
######################################################
# 需要修改部分结束，结果输出csv文件名为原文件名加“nodirection”
######################################################

nodirection = hasdirection + '_nodirection'
has_file = hasdirection + '.csv'
no_file = nodirection + '.csv'

df = pd.read_csv(has_file)
from_id = df[from_header].unique()
to_id = df[to_header].unique()
result_df = df.copy()
result_df.drop(result_df.index, inplace=True)
itemList = []  # 存储OD起终点，用于判断是否已经计算过
for from_item in from_id:
    for to_item in to_id:
        if from_item != to_item:
            forward = df.loc[(df[from_header] == from_item)
                             & (df[to_header] == to_item)]
            forward_item = str(from_item) + str(to_item)
            if forward_item in itemList:
                continue
            elif forward.empty:
                backward = df.loc[(df[from_header] == to_item) &
                                  (df[to_header] == from_item)]
                backward_item = str(to_item) + str(from_item)
                if backward_item in itemList:
                    continue
                elif backward.empty:
                    continue
                else:
                    itemList.append(backward_item)
                    result_df = pd.concat([result_df, backward])
            else:
                itemList.append(forward_item)
                vol_1 = forward[vol_header].values[0]
                backward = df.loc[(df[from_header] == to_item) &
                                  (df[to_header] == from_item)]
                backward_item = str(to_item) + str(from_item)
                if backward_item in itemList:
                    continue
                elif backward.empty:
                    continue
                else:
                    itemList.append(backward_item)
                    vol_2 = backward[vol_header].values[0]
                    vol_all = int(vol_1) + int(vol_2)
                    forward[vol_header] = vol_all
                # result_df.append(forward, ignore_index=True)
                result_df = pd.concat([result_df, forward])
result_df.to_csv(no_file, index=False, header=True)
