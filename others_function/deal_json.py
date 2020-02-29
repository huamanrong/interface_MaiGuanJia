__author__ = 'Administrator'
old_json = '''
Name: 潘腾虎
Birthday: 1990-10-18
Sex: 1
IDNumber: 350301199010180054
Nation: 汉
IDIssued: 莆田市公安局秀屿分局
Address: 福建省莆田市秀屿区笏石镇丙村大165号
userLife: 2015-11-20 至 2025-11-20
IssuedData: 20151120
ValidDate: 20251120
Base64Photo: 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
FrontImg:
backImg:
workerId: 182
Other:
CardNumber:
PhotoName: C:Program Files (x86)ZKIDROnlineinzp.bmp
ImageName:
Base64Image: (null)
fp_feature1: QwEEEgELSgAAAAAAAAAAAAAAACIBmjJoAP///////2E3kvwbO9D8T0uY/IlJMf5tWi3+NmPN/MtqMf56bnr8jnsk/kN8JP4tgA7+E4MU/sKNKv4tkGL8IJId/radI/4Lql78HLRr/CmyafxTy138PNdl/Azjefyn71L8NfNw/DP3gPw6+V38zPhP/EX9Q/wiGp39niU1/UwpFP2pJyz9b0MU/ZdTDv0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKo=
fp_feature2: QwEEEgEQSAAAAAAAAAAAAAAAACsBmnpgAP///////0wM2fwyGCb8aR0R/M8eRv6cOE3+wEc6/qdNNP5aUSX8EFc3/IJhN/7iaSf+Sm/2/HpwBv4sdvL8oHgb/q57IP6OhQf+8KIU/oioTfxRqw7+z64H/t6zCP5xuFf8nbtM/FTKZfzUzlL8dNZX/EPbKf715Ub8YfRX/lb6f/zn/y78JhWI/XYZD/1AIJL9vR4m/SQviP3QLRv9gzMO/ZszGP2/Rgb9rUgH/SxPiv0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACU=
CardType: 1
EnName:
CnName:
PassNum:
VisaTimes: 0
teamId: 133
companyId: 652
photo_url: https://gdkq.4000750222.com/gdsmzimages/test/7.jpg
cardno: 56465189451641561
'''


def deal_json(error_json):
    dict_param = {}
    list_param = list(filter(lambda x: x != '', error_json.split('\n')))
    for i in list_param:
        list_sub = i.split(':', 1)
        dict_param[list_sub[0]] = list_sub[1].strip()
    return dict_param

print(deal_json(old_json))