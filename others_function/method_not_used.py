__author__ = '10336'
import json

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
                value = self.get_contact_value(item, key)  # 调用get_contact_value()，获得值
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
