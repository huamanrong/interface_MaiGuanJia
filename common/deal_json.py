__author__ = 'Administrator'
old_json = '''
workId: 392
areaCode: 130102
projectId: 329
companyId: 792
workerId: 392
file: {"name":"王大锤.jpg","url":"https://gdkq.4000750222.com/gdsmzimages/test/王大锤.jpg","uid":1565948823169,"status":"success"}
id: 792
'''


def deal_json(error_json):
    dict_param = {}
    list_param = list(filter(lambda x: x != '', error_json.split('\n')))
    for i in list_param:
        list_sub = i.split(':', 1)
        dict_param[list_sub[0]] = list_sub[1].strip()
    return dict_param


print(deal_json(old_json))