import os

# 获得到的绝对地址到  ...\interface_automation\interface
project_conf_path = os.path.realpath(__file__).replace('common\project_path.py', '')

# 测试用例的路径
test_data_path = os.path.join(project_conf_path, 'test_data', 'test_interface.xlsx')

# http配置文件的路径
http_conf_path = os.path.join(project_conf_path, 'conf', 'http.conf')

# 日志路径
log_path = os.path.join(project_conf_path, 'test_result', 'log', 'test_log.txt')

# 测试报告路径
report_path = os.path.join(project_conf_path, 'test_result', 'html_report')

# 用例配置文件的路径
case_conf_path = os.path.join(project_conf_path, 'conf', 'case.conf')

# 数据库配置文件路径
db_conf_path = os.path.join(project_conf_path, 'conf', 'db.conf')

# 图片文件的路径
picture_path = os.path.join(project_conf_path, 'picture')

# yaml文件的路径
yaml_path = os.path.join(project_conf_path, 'conf' , 'global_variable.yaml')

# csv配置参数的文件路径
csv_param_path = os.path.join(project_conf_path, 'test_data', 'param')