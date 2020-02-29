__author__ = 'Administrator'
import yaml
from common import project_path


def yaml_fun():
    with open(project_path.yaml_path, encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
    # with open(project_path.yaml_path, 'w', encoding='utf-8') as file:
    #     yaml.dump(data, file)


if __name__ == '__main__':
    from common.my_log import MyLog
    # logger = MyLog().my_log()
    # logger.info('打卡了，啊哈哈')
    yaml_fun()
