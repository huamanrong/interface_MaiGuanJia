import unittest
import time
import HTMLTestRunnerNew
from common.send_email import SendEmail
from common.test_http_request import TestHttpRequest
from common import project_path

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.loadTestsFromTestCase(TestHttpRequest))

now = time.strftime('%Y-%m-%d_%H_%M_%S')
file_path = project_path.report_path+'\\test'+now+'.html'

# 执行用例
with open(file_path, 'wb') as file:
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title=None, description=None, tester='the great PTH')
    runner.run(suite)

#发送邮件
# send='1033674932@qq.com'
# pwd='*********'
# receiver='1033674932@qq.com'
# message='发送HTML的测试报告'
# Subject='测试报告'
# file_path='test2018.html'
# SendEmail(send,pwd,receiver,message,Subject).send_email_with_file(file_path)