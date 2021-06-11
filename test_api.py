import requests
import json
import datetime
from urllib import parse
from pprint import pprint
# print(parse.quote("中文"))
# print(parse.unquote())



# 查询素材图片接口参数


def endpayload(payload):
    payload = "json=" + str(parse.quote(str(payload)))
    return payload

def getimage(authToken):
    nowtime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    url = "https://pre-omo.aiyouyi.cn/api-decoration-web/decoration/api.do"
    p = {
        "head": {
            "target": "DECORATION-MY-FILE-LIST-PROCESSOR",
            "accessToken": authToken,
            "client": "3",
            "version": "vsesion-2.0.0.1",
            "requestTime": nowtime,
            "channel": "页面测试",
            "key": "133C9CB27DA0",
            "value": "d998dc351df60d397f85ea4e422ef423"
        },
        "data": {
            "cid": 999,
            "fileGroupInfoId": "",
            "startIndex": 1,
            "pageSize": 100,
            "sourceMaterialType": "0",
            "fileName": ""
        }
    }

    payload = endpayload(p)
    print(len(payload))
    print(payload)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '711',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'authToken='+authToken,
        'Host': 'pre-omo.aiyouyi.cn'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    file_list = json.loads(response.text).get('data').get('list')
    return file_list

def Create_api():
    url = "https://pre-omo.aiyouyi.cn/api-commodity-web/commodity/api.do"
    accessToken = '1'
    pname = 'pname'
    a = '{"head":{"target":"PRODUCT-NEW-PROCESSOR",' \
        '"accessToken":"884118fbfa41c50206de8f2312ae5e1f1e0d232bdd0b049796e8a2887805803f","client":"3","version":"vsesion-2.0.0.1",' \
        '"requestTime":"2021-06-01 13:06:41","channel":"页面测试","key":"133C9CB27DA0","value":"e5c6af475d5b39ad5ce71d76b45fcabc"},"data":{' \
        '"cid":999,"productCategoryInfoId":"206","productCatalogInfoIds":["1369557600303058979","1369558785017778248","1369558910918201352"],' \
        '"name":"商品名称001","description":"商品描述001","images":"https://pre-omo.aiyouyi.cn/web-file/999/image/336a9/ffc29546b2be4cc4aa41e41711be7e8e.jpg","productCategoryInfoIds":"","selfSaleCount":"20","productLabelId":"1399277926557421643","startSaleNum":1,"quantitySold":0,"status":1,"autoSaleTime":"","isJoinDiscount":1,"zhengsong":1,"isSupportInvoice":1,"isShowStock":1,"isShowSaleCount":1,"productUnit":"个","other":true,"otherUnit":"个","isCashOnDelivery":1,"isFreeFreight":0,"isAfterSaleService":1,"isShowRelationProduct":0,"relationProductInfoIds":[],"productDetail":"","pcDetail":"","goodsInfo":[],"goodsInfos":[{"codeErrorMessage":"","costPrice":"10","costPriceErrorMessage":"","fileList":[],"image":"","label":"红","labelArr":["红"],"salePrice":"12","salePriceErrorMessage":"","showCodeError":false,"showCodeSpan":false,"showCostPriceError":false,"showSalePriceError":false,"showStockError":false,"showVolumeError":false,"showWarningStockError":false,"showWeightError":false,"stock":"100","stockErrorMessage":"","volume":"0.1","volumeErrorMessage":"","warningStock":"50","warningStockErrorMessage":"","weight":"0.5","weightErrorMessage":"","specs":"{\"颜色1\":\"红\"}"},{"codeErrorMessage":"","costPrice":"10","costPriceErrorMessage":"","fileList":[],"image":"","label":"黄","labelArr":["黄"],"salePrice":"12","salePriceErrorMessage":"","showCodeError":false,"showCodeSpan":false,"showCostPriceError":false,"showSalePriceError":false,"showStockError":false,"showVolumeError":false,"showWarningStockError":false,"showWeightError":false,"stock":"100","stockErrorMessage":"","volume":"0.1","volumeErrorMessage":"","warningStock":"50","warningStockErrorMessage":"","weight":"0.5","weightErrorMessage":"","specs":"{\"颜色1\":\"黄\"}"},{"codeErrorMessage":"","costPrice":"10","costPriceErrorMessage":"","fileList":[],"image":"","label":"蓝","labelArr":["蓝"],"salePrice":"12","salePriceErrorMessage":"","showCodeError":false,"showCodeSpan":false,"showCostPriceError":false,"showSalePriceError":false,"showStockError":false,"showVolumeError":false,"showWarningStockError":false,"showWeightError":false,"stock":"100","stockErrorMessage":"","volume":"0.1","volumeErrorMessage":"","warningStock":"50","warningStockErrorMessage":"","weight":"0.5","weightErrorMessage":"","specs":"{\"颜色1\":\"蓝\"}"}],"freightTemplateId":"1153987269569418345","code":"","isRecommend":1,"itemCat":"","imageData":{"fileName":"image"},"productCatalogInfoId":"","generalExpressType":1,"businessDispatchType":1,"shopExtractType":1,"specsType":1}}' \
        # % (accessToken, pname)
    payload = "json=" + str(parse.quote(a))

    ContentLength = len(payload)
    print(ContentLength)
    headers = {
        'Content-Length': str(ContentLength),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'authToken=884118fbfa41c50206de8f2312ae5e1f1e0d232bdd0b049796e8a2887805803f',
        'Host': 'pre-omo.aiyouyi.cn'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

# for i in range(100):
#     Create_api()

if __name__ == '__main__':
    authToken = "884118fbfa41c50206de8f2312ae5e1f10d557ecf5264b81c2f564fd9145a0df"
    print(getimage(authToken))
