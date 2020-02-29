import unittest
import json
import yaml
import re
from ddt import ddt, data
from common.read_config import ReadConfig
from common.http_request import HttpRequest
from common.do_excel import DoExcel
from common.my_log import MyLog
from common.do_mysql import DoMysql
from common import project_path
from common.post_processor import PostProcessor
from common.config_element import ConfigElement

# 获取用例的执行模式
mode = ReadConfig().read_config(project_path.case_conf_path, 'CASE', 'mode')
case_list = eval(ReadConfig().read_config(project_path.case_conf_path, 'CASE', 'case_list'))

# 获取测试数据、ip地址
sheet = 'add_workers'
test_data = DoExcel(project_path.test_data_path, sheet).read_data(mode, case_list)
IP = ReadConfig().read_config(project_path.http_conf_path, 'HTTP', 'test_ip')

logger = MyLog().my_log()
post_processor = PostProcessor(logger)


@ddt
class TestHttpRequest(unittest.TestCase):
    def setUp(self):
        self.excel = DoExcel(project_path.test_data_path, sheet)
        with open(project_path.yaml_path, encoding='utf-8') as file:
            self.yaml_data = yaml.load(file, Loader=yaml.UnsafeLoader)
        logger.info("开始测试啦")

    @data(*test_data)
    def test_http_request(self, sub_data):
        logger.info("目前正在执行第%s条用例" % sub_data['case_id'])

        if re.search('randstrName_|increase_|randstr_|randint_', str(sub_data)):    # 判断是否要做参数配置
            sub_data = ConfigElement(logger).config_variable(sub_data, self.yaml_data)

        if re.search('\${.*?}', str(sub_data)):     # 判断是否要做参数替换或反射方法
            sub_data = post_processor.correlation_replace(sub_data, self.yaml_data)

        if sub_data['preposition_sql']:     # 判断是否有数据库前置处理
            post_processor.preposition_sql(eval(sub_data['preposition_sql']))

        param = eval(sub_data['param'])
        if re.search("{'base64':.*?}", str(param)):    # 处理需要用64位编码来编码图片
            param = ConfigElement(logger).deal_photo_base64(param)

        logger.info("测试数据是:{0}".format(sub_data['param']))

        res = HttpRequest(IP+sub_data['url'], param).http_request(sub_data['method'], payload=sub_data['json'], token=self.yaml_data['token'])
        try:
            response = json.loads(res.content.decode())
            logger.info('返回值为：%s' % res.text)
        except Exception as e:
            logger.error('返回值报错')
            logger.error('报错信息：%s' % res.text)
            raise e

        if ('/account/projectAccount/login' in sub_data['url']) and response['data'] != '':
            token = response['data']['Token']
            self.yaml_data['token'] = token

        if sub_data['correlation']:    # 判断是否要调用参数提取函数
            post_processor.correlation_save_dict(response, sub_data['correlation'], self.yaml_data)

        if sub_data['post_sql']:     # 判断是否要数据库后置处理
            post_processor.post_sql(eval(sub_data['preposition_sql']))

        try:
            logger.info('开始断言')
            contrast_result = post_processor.assert_result(eval(sub_data['expect_result']), response)
            self.assertEqual(True, contrast_result)
            logger.info('预期结果断言正确')
            result = 'Pass'
            self.excel.write_data(int(sub_data['case_id']) + 1, 'request', str(response), result)
        except AssertionError as e:
            result = 'Fail'
            logger.error('结果断言错误')
            self.excel.write_data(int(sub_data['case_id']) + 1, 'request', str(response), result)
            raise e

        if sub_data['check_sql']:
            query_sql = eval(sub_data['check_sql'])
            db = query_sql.get('ab') if query_sql.get('db') else 1
            sql_result = DoMysql(logger).do_mysql(query_sql['sql'], db=db)
            try:
                self.assertEqual(str(query_sql['expected']), str(sql_result))
                check_sql_result = 'PASS'
                logger.info('数据库结果断言正确')
                self.excel.write_data(int(sub_data['case_id']) + 1, 'sql_request', str(sql_result), check_sql_result)
            except AssertionError as e:
                check_sql_result = 'FAIL'
                logger.error('数据库结果断言错误')
                self.excel.write_data(int(sub_data['case_id']) + 1, 'sql_request', str(sql_result), check_sql_result)
                raise e

    def tearDown(self):
        with open(project_path.yaml_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.yaml_data, file)
        logger.info("结束测试了\n")
