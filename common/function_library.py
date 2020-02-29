__author__ = '10336'
import time
from common.my_log import MyLog


def time_sleep(seconds):
    log = MyLog().my_log()
    log.info('进入时间等待方法')
    if seconds.isdigit() or isinstance(seconds, int):
        time.sleep(int(seconds))
        log.info('等待时间%s秒' % seconds)
    else:
        log.info('参数seconds输入错误')
