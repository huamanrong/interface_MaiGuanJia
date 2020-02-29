__author__ = '10336'
'''
后置处理的相关方法:
    处理关联参数的相关方法
    断言相关方法
    数据库的前置处理和后置处理
'''
import re
import copy
from common.my_log import MyLog
from common import function_library
from common.do_mysql import DoMysql


class PostProcessor:
    def __init__(self, logger):
        self.logger = logger

    # 用来处理预期结果与实际结果的对比
    def assert_running(self, dict_except, dict_actual, list_result, key=None):
        if isinstance(dict_except, dict):
            for key in dict_except.keys():
                if key in dict_actual.keys():
                    # if contrast(dict_except[key], dict_actual[key]) != None:
                    self.assert_running(dict_except[key], dict_actual[key], list_result, key=key)
                else:
                    list_result.append('返回值中没有 %s 这个字段' % key)
        elif isinstance(dict_except, list):
            for list_except, list_actual in zip(dict_except, dict_actual):
                # if contrast(list_except, list_actual) != None:
                self.assert_running(list_except, list_actual, list_result)
        else:
            if str(dict_except) != str(dict_actual):
                list_result.append('实际值 %s=%s 不等于预期值 %s=%s' % (key, dict_actual, key, dict_except))

    # 用来处理预期结果与实际结果的对比,返回True说明对比成功,不成功则返回错误信息列表
    def assert_result(self, dict_except, dict_actual):
        list_result = []
        self.assert_running(dict_except, dict_actual, list_result)
        if not list_result:
            self.logger.info('对比成功^_^')
            return True
        else:
            self.logger.error('对比错误,错误信息:%s' % list_result)
            return list_result

    '******************************************************************'

    # 传入一个key在实际返回值中遍历，返回相同key的值
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

    def correlation_save_dict(self, dict_actual, contact, dict_global):
        '''
        ——后置参数提取方法——
        在接口返回值中获取关键字段，并存储在yaml中,书写格式：{'age':''}、json提取器格式:变量名.data.age.name或 正则提取(暂未实现)
        :param dict_actual: type:dict   实际返回值
        :param contact:  correlation单元格的内容,要进行获取的字段
        :param dict_global: type:dict    全局变量，用来存储关联参数的值
        :return: 无返回值。在实际返回值获取参数并存储在字典中
        '''
        self.logger.info('*_*进入参数提取方法*_*')
        try:
            contact = eval(contact)
        except:
            contact = contact
        if isinstance(contact, dict):
            for key in contact.keys():
                if dict_actual.get(key):
                    value = dict_actual[key]
                else:
                    value = self.get_contact_value(dict_actual, key)
                dict_global[key] = value
        elif isinstance(contact, str):
            contact = [contact]
        if isinstance(contact, list):
            for expression in contact:
                copy_dict_global = copy.deepcopy(dict_actual)
                express_li = expression.split('.')
                variable = express_li[0]
                express_li.pop(0)
                for i in express_li:
                    if re.search('\[\d+\]', i):
                        sub_var = re.search('\w+', i).group()
                        copy_dict_global = copy_dict_global[sub_var]
                        while re.search('\[\d+\]', i):
                            copy_dict_global = copy_dict_global[int(re.findall('\[(\d+)\]', i)[0])]
                            i = i.replace(re.search('\[\d+\]', i).group(), '', 1)
                    else:
                        copy_dict_global = copy_dict_global[i]
                    dict_global[variable] = copy_dict_global
        self.logger.info('*_*参数提取完成*_*')

    '******************************************************************************'

    def correlation_replace(self, data, dict_global):
        '''
        在请求之前判断如果各参数中有${}格式的字段，就使用字典里的值进行替换
        :param data: Excel整行的数据
        :param dict_global: 全局字典
        :return:返回替换完成的整行的数据
        '''
        while re.search('\${.*?}', str(data)):
            self.logger.info('*_*进入参数替换方法*_*')
            for key, value in data.items():
                if value is not None and not isinstance(value, int):
                    if re.search('__\w+\(.*?\)', value):    # 判断是不是要反射方法，否则就是变量
                        result_list = re.findall('\${__\w+\(.*?}', value)
                        result = value
                        for sub in result_list:
                            func_name = re.search('__\w+', sub).group().replace('__', '')
                            args = re.findall('__\w+\((.*?)\)', sub)[0].replace(' ', '').split(',')
                            args = tuple(map(lambda x: int(x) if x.isdigit() else x, args))   # 转化整形
                            try:
                                func_result = getattr(function_library, str(func_name))(*args)
                                func_result = '' if func_result is None else func_result
                            except Exception as e:
                                self.logger.error('调用函数库错误，检查书写是否正确')
                                raise e
                            if len(re.findall('__\w+\(.*?\)', sub)[0]) < len(re.findall('\${(__\w+\(.*?)}', sub)[0]):
                                func_result = eval(re.findall('\${(__\w+\(.*?)}', sub)[0].replace(re.findall('__\w+\(.*?\)', sub)[0], str(func_result)))
                            result = result.replace(sub, str(func_result))
                        data[key] = result
                    else:
                        result_list = re.findall('\${.*?}', value)
                        result = value
                        for sub in result_list:
                            variable = dict_global[re.search('\w+', sub).group()]
                            if len(re.findall('\w+', sub)) > 1:
                                variable = eval(re.findall('{(.*?)}', sub)[0].replace(re.search('\w+', sub).group(), str(variable)))
                            result = result.replace(sub, str(variable))
                        data[key] = result
        self.logger.info('*_*参数替换完成*_*')
        return data

    '******************************************************************************'

    def preposition_sql(self, sql_param):
        '''
        SQL前置处理,有更改、删除和新增操作，暂时不支持查询和参数提取操作
        :param sql_param: 单元格里的参数
        :return: 暂无返回
        '''
        self.logger.info('——进入SQL前置处理——')
        if isinstance(sql_param, dict):
            sql_param = [sql_param]
        for sub_sql in sql_param:
            sql = sub_sql['sql']
            db = sub_sql.get('db') if sub_sql.get('db') else 1
            DoMysql(self.logger).commit_mysql(sql, db=db)
        self.logger.info('——SQL前置处理完成——')

    def post_sql(self, sql_param):
        '''
        SQL后置处理,有更改、删除和新增操作，暂时不支持查询和参数提取操作
        :param sql_param: 单元格里的参数
        :return: 暂无返回
        '''
        self.logger.info('——进入SQL后置处理——')
        if isinstance(sql_param, dict):
            sql_param = [sql_param]
        for sub_sql in sql_param:
            sql = sub_sql['sql']
            db = sub_sql.get('db') if sub_sql.get('db') else 1
            DoMysql(self.logger).commit_mysql(sql, db=db)
        self.logger.info('——SQL后置处理完成——')

if __name__ == '__main__':
    logger1 = MyLog().my_log()
    ss = {'request_type': None,
     'case_id': 1,
     'correlation': None,
     'json': None,
     'method': 'post',
     'expect_result': "{'age': '${__age(hello,world)}','pen':'ios_increase_0001','apple':'increase_5','ran':'randstr_3'}",
     'param': "{'teamId': '${teamId+1}', 'companyId': '${companyId+1}', 'Base64Photo': {'base64':'120KB.jpg'},"
              "'home':'randint_5', 'ting':'randint_00000','xingyun':'idrandint_5','luo':'350301randint_000'}",
     'check_sql': "{'sql':'select * ${age+6}','execept':'randstrName_3'}",
     'url': '/zuul/zuulPersonnel/personnel/person/addWorker'}
    test_dict = {'expect_result': "{'age': '${age**2}','pen':'ios_increase_0001','apple':'increase_5','ran':'randstr_3'}"}
    post = PostProcessor(logger1)
    # res = post.correlation_replace(ss,{'age':18, 'teamId':50, 'companyId': 10})
    # print(res)
    act = {'code': 0, 'data1': [['age', 'hobby', [1, {'name': 'xiaohong'}]], ['name']], 'message': 'SUCCESS', 'data':
        {'id': 1634, 'name': '习中邓', 'idcard': '513436199008018603', 'corpname': '北京爱奇艺科技有限公司', 'teamName': '分包-电影班', 'status': 0,}}
    con = "['idcard.data.idcard', 'name.data.name', 'bo.data1[0][2][1].name']"
    gol = {}
    post.correlation_save_dict(act, con, gol)
    print(gol)
