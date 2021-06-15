import json
import sys
import requests
import time
from public_mods.login_b_c import Environment
from public_mods.Common_method import Common


class Order(Environment):

    def go_shop(self,goods):
        try:
            self.driver2.get(goods)
            #下单
            #WebDriverWait(self.driver2,5,1).until(EC.presence_of_element_located((By.XPATH,'//div[@class="img-close-home')))
            time.sleep(2)
            self.driver2.find_element_by_xpath('//button[@class="buy-now-btn sku-click"]').click()
            time.sleep(2)
            self.driver2.find_element_by_xpath('//button[@class="btn-sku-enter"]').click()
            time.sleep(3)

            #提交订单
            self.driver2.find_element_by_xpath('//button[@class="order-btn van-button van-button--primary van-button--normal"]').click()
            time.sleep(2)
            self.driver2.find_element_by_xpath('//button[@class="goOrder van-button van-button--default van-button--normal"]').click()
            time.sleep(2)
            ordercode=self.driver2.find_element_by_id('item-code').text
            print("下单成功")
            return ordercode

        except Exception as e :
            print("下单异常，操作失败",e)
    #确认收货
    def take_goods(self):
        try:
            self. driver2.refresh()
            time.sleep(2)
            self.driver2.find_element_by_xpath('//div/div[3]/button[1]').click()
            time.sleep(1)
            self.driver2.find_element_by_xpath('/html/body/div[1]/div[5]/div[2]/div[2]/div/button[2]').click()
            time.sleep(2)
            if self.driver2.find_element_by_xpath('//p[@class="order-status"]').text =="交易已完成":
                print("收货完成，测试结束...")
        except Exception as e:
                print("确认收货异常，请排查...\n",e)

    #从登录时存储的token文件里获取B端用户token
    def get_token1(self):
        path=self.get_path()
        with open(path, "r") as f:
            txt=f.read()
            txt=txt.split(':')[1]
            print(txt)
            return txt
    #获取B端用户token方法2
    def get_token(self,path):
        try:
            if "env_config_omo" in path:
                 with open("../userdata/内部测试0043/无一店铺D/accessToken.txt", "r") as f:
                    txt=f.read()
                    txt=txt.split(':')[1]
            elif "env_config_pre" in path:
                 with open("../userdata/内部测试0025/预发固定店铺二组1/accessToken.txt", "r") as f:
                    txt=f.read()
                    txt=txt.split(':')[1]
            else:
                 with open("../userdata/admin-mdl/麦当劳222店/accessToken.txt", "r") as f:
                    txt=f.read()
                    txt=txt.split(':')[1]
            return txt
        except Exception as e:
            print("获取商户token失败:",e)

    def queryOrder(self,code,token):
        url="https://omo.aiyouyi.cn/order/b/queryOrderList"
        header={"Accept":"application/json, text/plain, */*",
                "accessToken":token,
                "Connection":"keep-alive",
                "Content-Type":"application/json;charset=UTF-8"}
        data={"cid":3195,"shopId":3195,"currentPage":1,"pageSize":20,"data":{"currentPage":1,"pageSize":20,
                "searchType":"orderIdList","searchValue":code,"searchType2":"cpin","searchValue2":"",
                "orderIdList":[code],"orderPlatformId":"","orderPlatform":0,"type":"resetForm",
                "undefinedStart":"","createTimeEnd":"","cid":3195,"shopId":3195}}
        requests.post(url=url,headers=header,json=data)

    def delivery(self,code,token,data):
        try:
            data=eval(data)
            url="https://omo.aiyouyi.cn/order/b/batch/delivery"
            header={"Accept":"application/json, text/plain, */*",
                    "Connection":"keep-alive",
                    "Content-Type":"application/json;charset=UTF-8"}
            res = requests.post(url=url, headers=header, json=data)

            return res.text
        except Exception as e:
            print("发货异常:",e)





if __name__ == '__main__':
    com = Common()
    args = sys.argv
    if len(args) > 1:
        config_file=args[1]
    else:
        config_file = com.get_path()

    config = com.read_env_config(config_file)
    #B端登录
    env = Order("pc-b-login",config["pc-b-login"])
    success=env.run_login_b()
    #C端登录
    iphone=config["h5-c-login"]["iphone"]
    password=config["h5-c-login"]["password"]
    nickname=config["h5-c-login"]["nickname"]
    login_url=config["h5-c-login"]["login_url"]
    goods_url=config["h5-c-login"]["goods_url"]
    data=config["delivery-data"]["data"]
    code = env.login_c(iphone, password,nickname,login_url)
    order_code= env.go_shop(goods_url)   #购物下单,获取订单号
    # 发货
    if success==True:
        if len(order_code)>0:
            token=env.get_token(config_file)
            delivery_code=env.delivery(order_code, token,data)
            if "success" == json.loads(delivery_code)["status"]:
                print("发货成功")
                time.sleep(2)
                env.take_goods()   #确认收货
            else:
                print("发货失败")

    else:
        print("B端账号登录失败")

    # token=env.get_token()
    # print(token)
    # delivery_code=env.delivery("D1402820514841366590", token,data)
    # print(delivery_code)
