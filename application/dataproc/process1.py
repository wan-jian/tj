# coding=utf-8

import os
import sys
import pandas as pd
import numpy as np


def process1_1(process):

    # 处理在编教职工

    file_path = os.path.join(process['data_dir'], process['source_file'][0])
    df1 = pd.read_excel(file_path, sheet_name='在职', dtype={'职工号': str, '手机号码': str})

    file_path = os.path.join(process['data_dir'], process['source_file'][1])
    df2 = pd.read_excel(file_path, dtype={'职工号': str, '证件号码': str, '手机号码': str})

    df = merge_by_number(df1, df2)
    validate(df)

    if process['check_only'].upper() != 'YES':
        df['体检职别'] = np.nan
        df['怀孕'] = np.nan
        df['VIP'] = np.nan
        df['职务'] = np.nan
        df['在职情况'] = np.nan
        df['邮箱'] = np.nan
        df['备注'] = np.nan
        df['卡类型'] = np.nan
        df['卡号码'] = np.nan
        for i in df.index:
            if df.loc[i, '任职级别'] in ('正厅级', '副厅级') or df.loc[i, '职称级别'] in ('正高', '副高'):
                df.loc[i, '体检职别'] = '厅局级、高级职称干部'
            else:
                df.loc[i, '体检职别'] = '处及处以下干部职工'
            df.loc[i, '怀孕'] = '否'
            df.loc[i, '在职情况'] = '在职'
            df.loc[i, '备注'] = '<A> ' + df.loc[i, '选择医院']

        columns = ['姓名_x', '证件号码', '手机号码_x', '体检职别', '婚姻状况', '怀孕', 'VIP', '部门', '在职情况', '邮箱',
                   '备注', '卡类型', '卡号码']
        df = df[columns]
        df.rename(columns={'姓名_x': '姓名', '证件号码': '身份证号', '手机号码_x': '手机', '婚姻状况': '婚否'}, inplace=True)
        df_output1 = df

    # 处理退休教职工

    file_path = os.path.join(process['data_dir'], process['source_file'][0])
    df1 = pd.read_excel(file_path, sheet_name='退休', dtype={'职工号': str, '手机号码': str})

    file_path = os.path.join(process['data_dir'], process['source_file'][2])
    df2 = pd.read_excel(file_path, dtype={'职工号': str, '身份证号': str, '联系电话': str})

    df = merge_by_number(df1, df2)
    validate(df)

    if process['check_only'].upper() != 'YES':
        df['体检职别'] = np.nan
        df['怀孕'] = np.nan
        df['VIP'] = np.nan
        df['职务'] = np.nan
        df['在职情况'] = np.nan
        df['邮箱'] = np.nan
        df['备注'] = np.nan
        df['卡类型'] = np.nan
        df['卡号码'] = np.nan
        for i in df.index:
            if df.loc[i, '享受级别'] in ('正厅级', '副厅级', '正高', '正高级', '副高', '副高级'):
                df.loc[i, '体检职别'] = '厅局级、高级职称干部'
            else:
                df.loc[i, '体检职别'] = '处及处以下干部职工'
            df.loc[i, '怀孕'] = '否'
            df.loc[i, '在职情况'] = '退休'
            df.loc[i, '备注'] = '<A> ' + df.loc[i, '选择医院']

        columns = ['姓名_x', '身份证号', '手机号码', '体检职别', '婚姻状况', '怀孕', 'VIP', '部门', '在职情况', '邮箱',
                   '备注', '卡类型', '卡号码']
        df = df[columns]
        df.rename(columns={'姓名_x': '姓名', '手机号码': '手机', '婚姻状况': '婚否'}, inplace=True)
        df_output2 = df

    if process['check_only'].upper() != 'YES':
        df = pd.concat([df_output1, df_output2], ignore_index=True)
        df1 = df[df['身份证号'].str.len() == 18]
        df2 = df[df['身份证号'].str.len() != 18]

        file_path1 = os.path.join(process['data_dir'], process['output_file'][0])
        df1.to_excel(file_path1, index=False, header=True)

        file_path2= os.path.join(process['data_dir'], process['output_file'][1])
        df2.to_excel(file_path2, index=False, header=True)

        print('成功生成文件："{}"和"{}"'.format(file_path1, file_path2))


def validate(df):
    '''
    检查数据
    :param df:
    :return:
    '''
    result = True
    for index, row in df.iterrows():
        err = ''
        if row['姓名_x'] != row['姓名_y']:
            err = err + '\t<姓名不一致>"{}":"{}"'.format(row['姓名_x'], row['姓名_y'])

        if '手机号码' in row.index:
            phone = row['手机号码']
        elif '手机号码_x' in row.index:
            phone = row['手机号码_x']
            if len(phone) != 11 or not phone.isdigit():
                err = err + '\t<手机号码错误>"{}"'.format(phone)

        if err != '':
            result = False
            sys.stderr.write(str(index) + "=> ")
            sys.stderr.write(err + '\n')

    return result


def merge_by_number(df1, df2):
    df = pd.merge(df1, df2, on='职工号', how='left')
    return df


