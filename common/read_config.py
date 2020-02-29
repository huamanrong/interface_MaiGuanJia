__author__ = 'zz'
import configparser


class ReadConfig:
    @staticmethod
    def read_config(file_path, section, option):
        cf = configparser.ConfigParser()
        cf.read(file_path, encoding='UTF-8')
        value = cf.get(section, option)
        return value

if __name__ == '__main__':
    from common import project_path
    value=ReadConfig().read_config(project_path.http_conf_path,'HEADER','header_json')
    print(eval(value))