__author__ = '10336'
import re

act = {'code': 0, 'data1': [['age', 'hobby'], ['name']], 'message': 'SUCCESS',
       'data': {'id': 1634, 'name': '习中邓', 'idcard': '513436199008018603', 'corpname': '北京爱奇艺科技有限公司',
                'teamName': '分包-电影班', 'status': 0, 'workerType': None, 'isImportant': None, 'phoneNumber': None,
                'type': None, 'openBank': None, 'account': None, 'arrivalDate': None, 'relativeName': None,
                'address': None, 'emergencyNumber': None, 'photoUrl': None, 'createTime': None, 'createUser': None,
                'modifyTime': None, 'modifyUser': None, 'leaveTime': None, 'teamId': 300, 'uploadStatus': None,
                'personGuid': 'BAB867E09C44439C8468A743471D0A2A', 'cardno': '5646518945164', 'hzUploadState': None}}
dict_global = {}
con = "['age.data1[0][1]', 'name.data1.name']"
express_li = con.split('.')
variable = express_li[0]
express_li.pop(0)
for i in express_li:
    if re.search('\[\d+\]', i):
        sub_var = re.search('\w+', i).group()
        act = act[sub_var]
        while re.search('\[\d+\]', i):
            act = act[int(re.findall('\[(\d+)\]', i)[0])]
            i = i.replace(re.search('\[\d+\]', i).group(), '', 1)
            dict_global[variable] = act
print(dict_global)
# print(re.search('\[\d+\]', con).group())
