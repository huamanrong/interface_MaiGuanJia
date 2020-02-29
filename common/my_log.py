from common import project_path
import logging


class MyLog:
    @staticmethod
    def my_log(log_name='auto_cases', level='DEBUG', file_path=project_path.log_path):
        logger = logging.getLogger(log_name)
        logger.setLevel(level)  # 日志收集器的级别

        # 输出渠道 相对路径
        fh = logging.FileHandler(file_path, encoding='UTF-8')
        sh = logging.StreamHandler()

        fh.setLevel(level)  # 输出渠道的级别
        sh.setLevel(level)

        formatter = logging.Formatter('[%(levelname)s]%(asctime)s %(module)s 行数:%(lineno)d [日志信息]:%(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        #对接日志收集器 以及输出渠道
        logger.addHandler(sh)
        logger.addHandler(fh)
        return logger


if __name__ == '__main__':
    loggers = MyLog().my_log()
    # for i in [1,2,3]:
    #     logger.info('%s'%i)
