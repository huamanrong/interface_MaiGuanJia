__author__ = 'Administrator'
from common.my_log import MyLog
logger=MyLog()
list_result=[]
def contrast(dict_except,dict_actual):
        if isinstance(dict_except, dict):
            for key in dict_except:
                if key in dict_actual.keys():
                    # if contrast(dict_except[key], dict_actual[key]) != None:
                        contrast(dict_except[key], dict_actual[key])
                else:
                    list_result.append('返回值中没有 %s 这个字段'%key)
                    logger.error('返回值中没有 %s 这个字段'%key)
            return list_result
        elif isinstance(dict_except, list):
            for list_except, list_actual in zip(dict_except,dict_actual):
                # if contrast(list_except, list_actual) != None:
                    contrast(list_except, list_actual)
        else:
            if str(dict_except) != str(dict_actual):
                list_result.append('实际值 %s 不等于预期值 %s '%(dict_actual,dict_except))

ccc={"status":"success","message":"kkk","data":{"pageIndex":2,"pageCount":1,"pageSize":10,"nextPage":2,"prevPage":1,"dataList":[{"total":5},{"nextPage":2}]},"code":"200"}
ddd={"status":"success","message":"kkk","data":{"pageIndex":1,"pageCount":2,"pageSize":10,"total":5,"nextPage":2,"prevPage":1,"dataList":[{"total":5},{"nextPage":2}]},"code":"200","timestamp":1540952873228}

dict1 = {"id": "503", "name": "kkk", "name1": "kkk", "info": {"uid":"2017","stuName":[{"uid":"2017"}]}}
dict2 = {"id": "503", "name": "kkk",  "name1": "kkk","info": {"uid":"2018","stuName":[{"uid":"2017"}]}}



# print(contrast(dict1,dict2))

def contrast_result(dict_except,dict_actual):
    list_res=contrast(dict_except,dict_actual)
    if len(list_res) == 0:
        logger.info('对比成功')
        return True
    else:
        logger.error('对比错误,%s'%list_result)
        return list_res

print(contrast_result(dict1,dict2))


ff=[{'age':18,'hh':18},{'datalist':'','param':{'filed':'','age':''}}]
hh=[{'age':18,'hh':18},{'datalist':'','param':{'filed':'','age':''}}]
























