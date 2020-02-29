import pymysql
from common.project_path import *
from common.read_config import ReadConfig


class DoMysql:
    def __init__(self, logger):
        self.logger = logger

    def do_mysql(self, sql, db=1):
        '''
        :param sql: SQL语句
        :param db: 选择的数据库
        :return:关于返回值：如果只有单个值单元素，返回单个值，如：1；多元素，返回列表，如：[1, 2, 3]
                 如果多个值单元素。返回列表，如：[1, 2, 3]；多元素，返回嵌套列表，如：[[33, '支付宝'], [35, '天猫商城']]
        '''
        config = eval(ReadConfig().read_config(db_conf_path, 'DATABASE', 'config'))
        config['database'] = ReadConfig().read_config(db_conf_path, 'DATABASE', 'database%s' % db)
        cnn = pymysql.connect(**config)
        cursor = cnn.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 1:
                if len(result[0]) == 1:
                    new_result = result[0][0]
                else:
                    new_result = list(result[0])
            else:
                new_result = []
                for i in result:
                    if len(i) == 1:
                        new_result.append(i[0])
                    else:
                        new_result.append(list(i))
            return new_result
        except Exception as e:
            self.logger.error('查询数据出错了，报错是:%s' % e)
        finally:
            cursor.close()
            cnn.close()

    def commit_mysql(self, sql, db=1):
        config = eval(ReadConfig().read_config(db_conf_path, 'DATABASE', 'config'))
        config['database'] = ReadConfig().read_config(db_conf_path, 'DATABASE', 'database%s' % db)
        cnn = pymysql.connect(**config)
        cursor = cnn.cursor()
        try:
            cursor.execute(sql)
            cnn.commit()
        except Exception as e:
            self.logger.error('数据库执行失败')
            cnn.rollback()
            raise e
        finally:
            cursor.close()
            cnn.close()


if __name__ == '__main__':
    # log = MyLog().my_log()
    # DoMysql(log).do_mysql()
    pass
