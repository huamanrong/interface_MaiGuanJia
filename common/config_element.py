__author__ = '10336'
'''
配置元件相关方法
有CSV参数化，对参数进行生成，比如生成随机数字、计数器和生成随机字符串
'''
import os
import re
import random
import base64
from common import project_path
from common.my_log import MyLog
surname = ['陈', '王', '潘', '苏', '唐', '郝', '覃', '习', '温', '李', '刘', '赵', '钱', '孙', '罗', '张', '李', '钟']
string = '山有木兮木有枝 心悦君兮君不知 人生若只如初见 何事秋风悲画扇 十年生死两茫茫 不思量自难忘 曾经沧海难为水' \
     '除却巫山不是云 玲珑骰子安 红豆入骨相思知不 知 只愿君心似我心 定不负相思意 平生不会相思才会 相思便害相思' \
     '愿得一心人 白头不相离 竹竿 何袅袅鱼尾何簁 簁 人面不知何 处去桃花依旧笑 春风去年 今日此门中人面 桃花相映' \
     '红梦回唐 朝我看到唐太 宗李世民贞 观之治 大治天下我看 到传奇女皇帝 武则天贞观遗风 尽显巾帼之威 我看到唐玄宗' \
     '李隆基开元 盛世造福天下 苍生我看到千 古名妃扬玉环 回眸一笑百 媚生的迷人风采 我看到文成 公主远 嫁 吐蕃使两族' \
     '人民和同为一家梦回唐朝与诗仙李白怀才不遇叹举杯消愁愁更愁 与诗圣杜甫遇“朱门酒肉臭路有冻死骨感世态' \
     '炎凉我与诗人王之涣登 鹳雀楼 吟欲穷千里目更  上一层楼 我与才子王维 吟独在异乡为 异客 每逢佳节 倍思亲 不浸' \
     '涌起思 乡之情 我与大 师李商隐共 吟春蚕到死丝方尽蜡 炬成灰泪始干 品爱情之忠 贞要有最朴 素的生活和最崇高的理' \
     '想即使明 日天寒地冻 路遥马亡 树的智慧在于志存高远 正如高  晓松所说 人生不应当只有苟且与当下 还应有诗和' \
     '远方 只有心 存着远方我们才能 勇往直 前 不至于像失 了罗盘的水手 有了目标 与方向 我们才能更好 地到达终点 ' \
     '为中华之崛 起而读书 立下了 这样志向的周恩 来未曾彷徨 引领着中国 走向富强 如果再让我做一次选 我仍选 择中国 ' \
     '选择核事业 邓稼先坚定的 志向使他在 核领域一往无前 智慧的大树 向着远方 于是它有了目标 和动力 智者若树 志存高远' \
     '壮岁从戎 曾是气吞残虏阵云高狼烽夜举 朱颜青鬓拥雕戈西戍笑 儒冠自来多误功名梦断 却泛扁舟吴楚漫悲歌伤怀吊古 烟波无' \
     '际望秦关何处叹流年又成虚度极目晴川展画屏地从桃塞接蒲城滩头鹭占清波立 原上人侵落照耕 去雁数行天际没孤云一点静中生 ' \
     '凭轩尽日不回首楚水吴山无限情名园花正 好娇红白百态竞春妆笑 痕添酒晕丰脸凝脂谁为试铝霜诗朋酒伴趁此日 流转风光尽夜游不妨' \
     '秉烛未觉是疏狂 茫茫一年一度烂漫离披似长 江去浪但要教啼莺语燕不怨 卢郎问春春道何曾去任蜂 蝶飞过东墙君看取年年 潘令河阳'


class ConfigElement:
    def __init__(self, logger):
        self.logger = logger

    def config_variable(self, data, dict_global):
        '''
        (randstrName_)|(increase_)|(randstr_)|(randint_)
        test_http_request模块的用例如果需要对参数进行处理，就会调用这个方法，该方法会调用以下的各个方法，下面的方法返回param
        config_variable处理完之后一并整条数据
        :return:self.param
        '''
        while re.search('randstrName_|increase_|randstr_|randint_', str(data)):
            self.logger.info('进入参数配置方法')
            for k, v in data.items():
                if v is not None and not isinstance(v, int):
                    v = v.replace(' ', '')
                    if 'randint_' in v:
                        data[k] = self.random_variable(v)
                    elif 'increase_' in v:
                        data[k] = self.increase_variable(v, dict_global)
                    elif 'randstrName_' in v or 'randstr_' in v:
                        data[k] = self.random_str(v)
        self.logger.info('参数配置完成^_^')
        return data

    def random_variable(self, param):
        '''
        生成随机数字组合
        生成随机数字组合，书写格式有 “randint_5”、“randint_00000”、“idrandint_5”、“350301randint_5”
        :return:返回处理之后的param
        '''
        self.logger.info('进入生成随机数字组合方法')
        result_list = re.findall('randint_\d+', param)
        for sub in result_list:
            num = sub.replace('randint_', '')
            if str(int(num)) == num:
                ran = random.randrange(10**(int(num)-1), 10**int(num))
            else:
                ran = random.randrange(10**(len(num)-1), 10**len(num))
            param = param.replace(sub, str(ran))
        return param

    def increase_variable(self, param, dict_global):
        '''
        生成计数器，可以按顺序生成编号，且不会重复,数字递增，步长为1，步长暂时不支持自定义
        书写格式：'ios_increase_0001'(可得 ios_0001)、'increase_0004'(可得 0004)、'increase_0'(可得 0 从0开始递增)
        注意：如果变量在全局变量中已存在，那起始值就从全局变量中引用，并会改变全局变量中的值
        :return:返回处理之后的param
        '''
        self.logger.info('进入计数器方法')
        result_list = re.findall("'\w+':'\w*increase_\d+", param)
        for sub in result_list:
            sub_list = sub.replace("'", '').split(':')
            num = re.search('increase_\d+', sub_list[1]).group().replace('increase_', '')
            if sub_list[0] in dict_global.keys():
                res_num = dict_global[sub_list[0]]
            else:
                res_num = int(num)
            dict_global[sub_list[0]] = res_num + 1
            if str(int(num)) == num:
                res_num = res_num
            else:
                res_num = '0'*(len(num)-len(str(int(num))))+str(res_num)
            param = param.replace(re.search('increase_\d+', sub_list[1]).group(), str(res_num))
        return param

    def random_str(self, param):
        '''
        生成随机字符串，如姓名
        书写格式： randstr_3 生成普通字符串   randstrName_3 生成姓名
        :return:返回处理之后的param
        '''
        self.logger.info('进入生成随机字符串方法')
        if re.findall('randstr_\d+', param):
            result_list = re.findall('randstr_\d+', param)
            for sub in result_list:
                num = sub.replace('randstr_', '')
                s = ''
                while len(s) < int(num):
                    sub_str = string[random.randrange(0, len(string))]
                    if sub_str != ' ':
                        s += sub_str
                param = param.replace(sub, s)
        elif re.findall('randstrName_\d+', param):
            result_list = re.findall('randstrName_\d+', param)
            for sub in result_list:
                num = sub.replace('randstrName_', '')
                last_name = surname[random.randrange(0, len(surname))]
                s = ''
                while len(s) < int(num)-1:
                    sub_str = string[random.randrange(0, len(string))]
                    if sub_str != ' ':
                        s += sub_str
                param = param.replace(sub, last_name+s)
        return param

    def deal_photo_base64(self, param):
        # 处理需要用64位编码来编码图片,Excel书写格式：'photobase64':{'base64':'1.jpg'}
        self.logger.info('开始处理图片，转换成base64')
        for k, v in param.items():
            if type(v) is dict and 'base64' in v.keys():
                photo_url = os.path.join(project_path.picture_path, v['base64'])
                with open(photo_url, 'rb') as file:
                    data = base64.b64encode(file.read())
                    param[k] = data
        self.logger.info('图片处理完成^_^')
        return param

if __name__ == '__main__':
    ss = {'request_type': None,
     'expect_result': "{'age': '${age}','pen':'ios_increase_0001','apple':'increase_5','ran':'randstr_3'}",
     'param': "{'teamId': '${teamId}', 'companyId': '${companyId}', 'Base64Photo': {'base64':'120KB.jpg'},'home':'randint_5', 'ting':'randint_00000','xingyun':'idrandint_5','luo':'350301randint_000'}",
     'check_sql': "{'sql':'select * ${sge}','execept':'randstrName_3'}"}
    res = ConfigElement('log').config_variable(ss, {'pen': 10})
    print(res)

