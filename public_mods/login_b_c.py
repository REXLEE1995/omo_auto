from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import os
import re
import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from public_mods.LocalStorage import LocalStorage
from public_mods.Common_method import *


class Environment(Common):
    def __init__(self, envname, config):
        self.envname = envname
        self.url = config["url"]
        self.username = config["username"]
        self.password = config["password"]
        self.shopname = config["shopname"]
        logging.info('环境:' + self.url)
        logging.info('用户:' + self.username)
        self.driver = self.initchrome(1)
        self.driver2 = self.initchrome(2)


    def initchrome(self,c):
        chrome_options = Options()
        chrome_app = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe'
        chrome_driver = r'E:\why\Python3.9.5\chromedriver.exe'
        if c==2:
            UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            mobileEmulation = {"deviceMetrics": {"width": 337, "height": 730, "pixelRatio": 3.0},"userAgent": UA}
            chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
            # mobileEmulation ={"deviceName": "iPhone 6"}
            # chrome_options.add_argument('--user-agent=iphone')

        chrome_options.binary_location = chrome_app
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                },
            "profile.managed_default_content_settings.images": 1
        }
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        )
        driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
        driver.maximize_window()
        return driver

    #登录B端
    def run_login_b(self):
        if not self.cookie_login():
            if self.account_login():
                print("账号密码登录执行完成")
                return True
            else:
                print("用户："+self.username+"_cookies和账密登录都失败了")
        else:
            print("cookies登录执行完成")
            return True

    # 使用账密登录
    def account_login(self):
        print("使用账密登录")
        self.delete_cookie_storage(self.driver)
        self.driver.get(url=self.url + '-subsys/denglu/login')
        self.driver.find_element_by_name("userName").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)
        self.driver.find_element_by_xpath("//*[text()='登 录']").click()
        time.sleep(2)
        while True:
            for elm in self.driver.find_elements_by_class_name("shopName"):
                if elm.text == self.shopname:
                    elm.click()
                    if self.is_login():
                        return True
                    else:
                        return False
            self.driver.find_element_by_class_name("btn-next").click()
            time.sleep(1)

    # 使用cookies登录
    def cookie_login(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        # 判断cookies文件是否存在
        print("使用cookies登录B端")
        if os.path.exists(
                "userdata/" + self.username + "/" + self.shopname + "/" + str(self.username) + "_cookies.pickle"):
            print("读取已有cookie信息")
            try:
                self.driver.get(self.url + "-subsys/denglu/login")
                cookies = pickle.load(open(
                    "userdata/" + self.username + "/" + self.shopname + "/" + str(self.username) + "_cookies.pickle",
                    "rb"))
                for cookie in cookies:
                    if cookie['name'] == "authToken":
                        self.driver.add_cookie(cookie)
                userInfo = pickle.load(open(
                    "userdata/" + self.username + "/" + self.shopname + "/" + str(self.username) + "_userInfo.pickle",
                    "rb"))
                shopInfos = pickle.load(open(
                    "userdata/" + self.username + "/" + self.shopname + "/" + str(self.username) + "_shopInfos.pickle",
                    "rb"))
                storage = LocalStorage(self.driver)
                storage['userInfo'] = userInfo
                storage['shopInfos'] = shopInfos
                time.sleep(2)
                self.driver.get(self.url + "/profile/profile")
                self.driver.refresh()
                if self.is_login():
                    return True
                else:
                    return False
            except Exception as e:
                print("cookie登录失败，错误：" + str(e))
        else:
            print("未检测到cookie信息")
            return False

    # 判断B端是否登录
    def is_login(self):
        for i in range(10):
            time.sleep(1)
            try:
                src = self.driver.page_source
                text_found = re.search(r'用户登录已经超时！', src)
                if text_found is not None:
                    print("检测到用户登录已经超时！")
                    return False
                if self.driver.find_element_by_class_name("shop_name").text == self.shopname:
                    print("检测到登录成功")
                    # print("存储userInfo、存储shopInfos-------------------")
                    self.save_storage()
                    # print("存储cookie、提取accessToken-------------------")
                    self.save_cookie()
                    return True
                else:
                    print("登录失败")
            except Exception as e:
                print("检查是否完成登录···")
        print("登录失败")
        return False

    # 保存浏览器缓存信息
    def save_storage(self):
        if os.path.exists("userdata/" + self.username + "/" + self.shopname + "/"):
            pass
        else:
            os.makedirs("userdata/" + self.username + "/" + self.shopname + "/")
        storage = LocalStorage(self.driver)
        userInfo = (storage["userInfo"])
        pickle.dump(userInfo, open(
            "userdata/" + self.username + "/" + self.shopname + "/" + str(self.username) + "_userInfo.pickle", "wb"))
        shopInfos = (storage["shopInfos"])
        pickle.dump(shopInfos, open(
            "userdata/" + self.username + "/" + self.shopname + "/" + str(self.username) + "_shopInfos.pickle", "wb"))

    # 保存cookies
    def save_cookie(self):
        if os.path.exists("userdata/" + self.username + "/" + self.shopname + "/"):
            pass
        else:
            os.makedirs("userdata/" + self.username + "/" + self.shopname + "/")
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open(
            "userdata/" + self.username + "/" + self.shopname + "/" + str(self.username) + "_cookies.pickle", "wb"))
        for cookie in self.driver.get_cookies():
            if cookie['name'] == "authToken":
                filename = "userdata/" + self.username + "/" + self.shopname + "/" + "/accessToken.txt"
                with open(filename, 'w') as file_object:
                  file_object.write("accessToken:" + cookie['value'])


    # 登录c端h5
    def login_c(self,phone,password,nickname,login_url):
        print("C端开始登录...")
        self.driver2.get(login_url)
        time.sleep(1)
        self.driver2.find_element_by_xpath('//div[@id="app"]/div[2]/div[1]').click()  # 点击密码登录
        time.sleep(1)
        self.driver2.find_element_by_xpath(
            '//form[@class="form-data-wrap van-form"]/div[1]/div/div/input[@name="phone"]').send_keys(phone)
        self.driver2.find_element_by_xpath(
            '//form[@class="form-data-wrap van-form"]/div[4]/div/div/input[@name="password"]').send_keys(password)
        time.sleep(1)
        self.driver2.find_element_by_xpath('//*[@id="app"]/div[1]/form/button').click()  # 登录
        if self.is_long_c()==True:
            return True
            #通过浏览器缓存用户信息判断是否登录成功
            # storage = SessionStorage(self.driver2)
            # print(storage)
            # print(storage["userInfo"]["nickName"])
            # if storage["userInfo"]["nickName"]==nickname:
            #     self.driver2.get(goods)

    #判断是否c端登录成功
    def is_long_c(self):
        for i in range(10):
            time.sleep(1)
            try:
                if self.driver2.find_element_by_xpath('//*[@id="mobileNav"]/nav/div[3]/a/div[2]').text=="购物车":
                    print("C端登录成功")
                    return True

                else:
                    print("C端登录检测次数：",i)
            except Exception :
              print("检查是否完成登录···")

        return False


# if __name__ == '__main__':
#     config_file = "configs/env_config_omo.toml"
#     config = read_env_config(config_file)   #读取配置文件
#     # if config:
#     #     for c in config:
#     #         if c == "pc-b":
#     #             env = Environment(c, config[c])
#     #             env.run_login_b()
#     #
#     env = Environment("pc-b-login",config["pc-b-login"])  #初始化化浏览器
#     env.run_login_b()            #登录B端


