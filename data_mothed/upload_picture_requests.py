__author__ = 'Administrator'
import requests
from PIL import Image
from common.http_request import HttpRequest
import json
Token=''
url='http://xiaolaiapi.yinglai.ren/api-ucenter/app-api/app/login'

param={'appId':1000,'phone':13819480735,'password':12345678,'versionId':10044,'deviceType':'ANDROID'}

result=requests.post(url,param)
json_1=result.json()
if ('api-ucenter/app-api/app/login' in url) and json_1['data'] !='':
    token=json_1['data']['token']
    Token=token
    print(Token)
else:
    print('没获取到token')

# url_2='http://xiaolaiapitest.yinglai.ren/api-file/app-api/app/upload'
# url_21='http://xiaolaiapi.yinglai.ren/api-file/app-api/app/upload'
# file_path=r'D:\Backup\我的文档\GitHub\interface_automation\interface\picture\xiaowang.jpg'
# file_path_2=r'D:\Backup\我的文档\GitHub\interface_automation\interface\picture\test.jpg'
#
# image=[('file',('test.jpg',open(file_path_2,'rb'),'image/jpg')),('file',('test.jpg',open(file_path,'rb'),'image/jpg'))]
# # image={'file':('xiaowang.jpg',open(file_path,'rb'),'image/jpg')}
# header={'token':Token,'versionId':'10044','deviceType':'ANDROID','appId':'1000'}
# image_1={'token':'','versionId':'10036','deviceType':'ANDROID','appId':'1000','filename':['test.jpg']}
# from common.deal_data import DealData
# pic=DealData().picture_upload(image_1,'10044',Token)
# response=requests.post(url_21,headers=pic['headers'],files=pic['files'])
# print(response.text)
import os
from common.project_path import *

url_21='http://xiaolaiapi.yinglai.ren/api-file/app-api/app/upload'
param_1={'token':Token,'versionId':'10044','deviceType':'ANDROID','appId':'1000','filename':['test.jpg']}
# headers={'token':Token,'versionId':'10044','deviceType':'ANDROID','appId':'1000'}
# files=[('file', open(os.path.join(picture_path,'test.jpg'),'rb'))]
#('file',open('D:\\Backup\\我的文档\\GitHub\\interface_automation\\interface\\picture\\xiaowang.jpg','rb'), 'image/jpg')]
http=HttpRequest(url_21,param_1).http_request('post')
# result_1=http.http_request('post').text
# result_1=requests.post(url_21,headers=headers,files=files).text
# print(result_1)
# print(http.text)
#shareDynId=0&shareTopicId=0&latitude=&address=&topicId=0&imageList=%5B%7B%22imageHeight%22%3A400%2C%22imageId%22%3A%224081%22%2C%22imageUrl%22%3A%22http%3A%2F%2Fxiaolaiimage.yinglai.ren%2Funsafe%2F2019%2F01%2F04%2F09450002034466974.jpg%22%2C%22imageWidth%22%3A400%7D%2C%7B%22imageHeight%22%3A750%2C%22imageId%22%3A%224082%22%2C%22imageUrl%22%3A%22http%3A%2F%2Fxiaolaiimage.yinglai.ren%2Funsafe%2F2019%2F01%2F04%2F09450006337185914.jpg%22%2C%22imageWidth%22%3A750%7D%5D&dynamicPath=&tok&location=&versionId=10044&appId=1000&deviceType=ANDROID&token=
url_3='http://xiaolaiapi.yinglai.ren/api-moment/app-api/moments/publish'
image_list=json.dumps([{'imageHeight':1188,'imageId':4088,'imageUrl':'http://xiaolaiimage.yinglai.ren/unsafe/2019/01/10/14401300000928228.jpg','imageWidth':1080}])
# header={'Content-Type':'application/json; charset=UTF-8'}
print(type(image_list))
print(image_list)
param_3={'imageList':image_list,'token':Token,'content':'你好啊','versionId':'10044','appId':'1000','deviceType':'ANDROID','shareTopicId':0,'topicId':0,'shareDynId':0,'dynamicPath':''}
result=requests.post(url_3,param_3).text
print(result)


kk=[{'imageHeight':'$()','imageId':'$()','imageUrl':'$()','imageWidth':'$()'}]
















