__author__ = '10336'
from common.my_log import MyLog
from common.project_path import *
import base64
import os
import json


class DealData:
    def __init__(self, logger):
        self.logger = logger

    # 用来处理预期结果与实际结果的对比,返回True说明对比成功
    def contrast(self, dict_except, dict_actual, list_result, key=None):
        if isinstance(dict_except, dict):
            for key in dict_except.keys():
                if key in dict_actual.keys():
                    # if contrast(dict_except[key], dict_actual[key]) != None:
                        self.contrast(dict_except[key], dict_actual[key], list_result, key=key)
                else:
                    list_result.append('返回值中没有 %s 这个字段' % key)
        elif isinstance(dict_except, list):
            for list_except, list_actual in zip(dict_except, dict_actual):
                # if contrast(list_except, list_actual) != None:
                    self.contrast(list_except, list_actual, list_result)
        else:
            if str(dict_except) != str(dict_actual):
                list_result.append('实际值 %s=%s 不等于预期值 %s=%s' % (key, dict_actual, key, dict_except))

    # 用来处理预期结果与实际结果的对比,返回True说明对比成功,不成功则返回错误信息列表
    def contrast_result(self, dict_except, dict_actual):
        list_result = []
        self.contrast(dict_except, dict_actual, list_result)
        if len(list_result) == 0:
            self.logger.info('对比成功')
            return True
        else:
            self.logger.error('对比错误,错误信息:%s' % list_result)
            return list_result

    #处理需要用64位编码来编码图片,Excel书写格式：'photobase64':{'base64':'1.jpg'}
    def deal_photo_base64(self, params):
        for k, v in params.items():
            if type(v) is dict and 'base64' in v.keys():
                photo_url = os.path.join(picture_path, v['base64'])
                with open(photo_url, 'rb') as file:
                    data = base64.b64encode(file.read())
                    params[k] = data
        return params

    #传入一个key在实际返回值中遍历，返回相同key的值
    def get_contact_value(self, dict_actual, contact_key):
        if isinstance(dict_actual, dict):
            for key in dict_actual.keys():
                if key == contact_key and isinstance(dict_actual[key], (str, int, float)):
                    return dict_actual[key]
                else:
                    if self.get_contact_value(dict_actual[key], contact_key) is not None:
                        return self.get_contact_value(dict_actual[key], contact_key)
        elif isinstance(dict_actual, list):
            for item in dict_actual:
                if self.get_contact_value(item, contact_key) is not None:
                    return self.get_contact_value(item, contact_key)

    #调用get_contact_value函数，接口请求结束后，correlation单元格不为空，则使用correlation单元格的内容，
    #在接口返回值中获取关键字段，并存储在字典中
    def correlation_save_dict(self, dict_actual, contact, dict_global):
        '''
        :param dict_actual: type:dict   实际返回值
        :param contact: type:dict   correlation单元格的内容,要进行获取的字段
        :param dict_global: type:dict    全局变量，用来存储关联参数的值
        :return: 无返回值。在实际返回值获取参数并存储在字典中
        '''
        if type(contact) == dict:
            contact1 = contact
        else:
            contact1 = contact[0]
        for key in contact1.keys():
            if dict_actual.get(key):
                value = dict_actual[key]
            else:
                value = self.get_contact_value(dict_actual, key)
            if contact1[key] == '':
                dict_global[key] = value
            elif isinstance(contact1[key], str):
                dict_global[contact1[key]] = value
            elif isinstance(contact1[key], tuple):
                for key1 in contact1[key]:
                    dict_global[key1] = value

    # dynamicPath':[{'dynamicPath':''},{'shareDynId':''}]
    # dynamicPath':[{'dynamicPath':''},1]
    # 在请求之前判断request_type，如果是correlation且param中$，就使用字典里的值进行替换
    def correlation_replace(self, param, dict_global):
        if isinstance(param, dict):
            for key in param.keys():
                if key in dict_global.keys() and param[key] == '$':
                    param[key] = dict_global[key]
                elif type(param[key]) in (dict, list):
                    self.correlation_replace(param[key], dict_global)
            for key1 in param.keys():
                if type(param[key1]) in (list, tuple):
                    param[key1] = json.dumps(param[key1])
            return param
        elif isinstance(param, list):
            for list_1 in param:
                self.correlation_replace(list_1, dict_global)

    #用来处理有排序、有按某种规律显示、或者返回值有列表，要获取列表的中的值，
    # 处理方式：遍历到指定data_list的时候，遍历列表元素，提取要对比的值，添加一个列表中，返回列表
    def get_data_list(self, dict_actual, list_name):
        '''
        :param dict_actual: 实际返回的json
        :param list_name: 要遍历的list_name
        :return:返回列表
        '''
        if isinstance(dict_actual, dict):
            for key in dict_actual.keys():
                if key == list_name and isinstance(dict_actual[key], list):
                    return dict_actual[key]
                else:
                    if self.get_data_list(dict_actual[key], list_name) is not None:
                        return self.get_data_list(dict_actual[key], list_name)
        elif isinstance(dict_actual, list):
            for item in dict_actual:
                if self.get_data_list(item, list_name) is not None:
                    return self.get_data_list(item, list_name)

    #把参数存到字典中，再把一个列表的每一条的字典按顺序存到列表中去，下一步需要操作时， 在列表中按顺序提取并完成替换就可以
    def list_correlation_save_dict(self, dict_actual, correlation, dict_global):
        '''
        :param dict_actual:实际的json返回值
        :param correlation: 在correlation单元格中，存储有列表名称及要存储的字段，比如{'list_name':'dataList1','param':{'age':'','sex':''}}
        :param dict_global:  type:dict   用来存储关联列表的全局变量
        '''
        if type(correlation) == dict:
            data_list_name = correlation['list_name']
            param = correlation['param']
        else:
            data_list_name = correlation[0]['list_name']
            param = correlation[0]['param']
        data_list = self.get_data_list(dict_actual, data_list_name)  # 调用get_data_list函数，获得存储页面信息的列表
        list_1 = []
        for item in data_list:
            dict_1 = {}
            for key in param.keys():
                if item.get(key):
                    value = item[key]
                else:
                    value = self.get_contact_value(item, key)  # 调用get_contact_value，获得值
                if param[key] == '':
                    dict_1[key] = value
                elif isinstance(param[key], str):
                    dict_1[param[key]] = value
                else:
                    for key1 in param[key]:
                        dict_1[key1] = value
            list_1.append(dict_1)
        dict_global[data_list_name] = list_1

    #在请求之前，判断request_type如果是list_correlation，如果param中有$，就使用全局变量字典中的值进行替换
    def list_correlation_middle(self, param, data_list):
        if isinstance(param, dict):
            for key in param.keys():
                if key in data_list[0].keys() and str(param[key]).find('$') != -1:
                    param[key] = data_list[int(param[key].replace('$', ''))-1][key]
                elif type(param[key]) in (dict, list):
                    self.list_correlation_middle(param[key], data_list)
            for key1 in param.keys():
                if type(param[key1]) in (list, tuple):
                    param[key1] = json.dumps(param[key1])
            return param
        elif isinstance(param, list):
            for list_1 in param:
                self.list_correlation_middle(list_1, data_list)

    #在请求之前，判断request_type如果是list_correlation，如果param中有$，就使用全局变量字典中的值进行替换
    def list_correlation_replace(self, param, dict_global):
        list_1 = dict_global[param['list_name']]
        result_param = self.list_correlation_middle(param, list_1)
        result_param.pop('list_name')
        return result_param

    def sql_replace(self, sql, dict_global):
        if 'replace' in sql.keys():
            if 'type' not in sql.keys():
                dict_sub = dict_global
            elif 'type' in sql.keys() and sql['type'] > 0:
                dict_sub = dict_global[sql['list_name']][sql['type']-1]
            for item in sql['replace']:
                if type(item) == str:
                    sql['sql'] = sql['sql'].replace('$', str(dict_sub[item]), 1)
                elif type(item) == list:
                    count = 0
                    for index, value in enumerate(sql['expected']):
                        if value == '$':
                                sql['expected'][index] = dict_sub[item[count]]
                                count += 1
            sql.pop('replace')
            if 'list_name' in sql.keys():
                sql.pop('list_name')
        return sql


    def simple_sql_replace(self, sql, dict_global):
        if 'replace' in sql.keys():
            if 'type' not in sql.keys():
                dict_sub = dict_global
            elif 'type' in sql.keys() and sql['type'] > 0:
                dict_sub = dict_global[sql['list_name']][sql['type']-1]
            else:
                dict_sub = dict_global
            for item in sql['replace']:
                if type(item) == str:
                    sql['sql'] = sql['sql'].replace('$', str(dict_sub[item]), 1)
            sql.pop('replace')
            if 'list_name' in sql.keys():
                sql.pop('list_name')
        return sql

if __name__ == '__main__':
    import time
    logger1 = MyLog().my_log()
    time_1 = time.time()
    deal = DealData(logger1)
    d1 = {"code": 1,"message":"操作成功","data":[{"enterpriseStatus":1,"employeeId":315,"enterpriseId":3,"enterpriseName":"演示账号"}]}
    d2 = {"code": 1,"message":"操作成功","data":[{"image":"https://kq.4000750222.com/kqimages/file/2019/7/9/2c90ef856bd4ad9d016bd4ad9d2d0000.jpg","enterpriseStatus":1,"employeeId":355,"enterpriseId":2,"enterpriseName":"演示账号"}]}
    # result = deal.contrast_result(d1, d2)
    # print(result)
    dd = {}
    dc = {'age': 18,'photo':{'base64':'120KB.jpg'}}
    deal.deal_photo_base64(dc)
    print(dc)