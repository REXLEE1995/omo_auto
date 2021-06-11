import toml
import tkinter as tk
from tkinter import filedialog

class Common(object):

    def get_path(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        return file_path

    def read_env_config(self,config_file):
        try:
            temp_dict = {}
            file_a = config_file
            configs = toml.load(file_a)   #解析成字典返回

            # for key in configs:
            #     if configs[key]["status"] == "true":
            #         temp_dict[key] = configs[key]
            return configs
        except Exception as e:
            print("配置文件有误，请检查！")
            print(e)
            return False

    def get_elem(self,driver,path,vale):
        driver.find_element(path,vale)
# 清除缓存
    def delete_cookie_storage(self,driver):
        driver.delete_all_cookies()

    # 退出浏览器
    def endchrome(self,driver):
        driver.quit()



