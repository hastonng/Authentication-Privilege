import traceback

import requests
import json
import time
import sys

from util_process import get_working_path, write_data, clear_download_folder

syms = ['\\', '|', '/', '-']


def w3_login(username, password):
    """
     Login into Huawei W3 Domain to authorised all system for exports
    :param username: String
    :param password: String
    :return: requests.Session
    """
    print('\n')
    print('Login to W3 Domain as: ' + username)
    print('\n')
    session = requests.session()
    firstHeader = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-TW,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'login.huawei.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    }
    firstURL = 'https://login.huawei.com/login/'
    resultA = session.get(firstURL, headers=firstHeader)
    header1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Host': 'login.huawei.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://login.huawei.com',
        'Referer': 'https://login.huawei.com/login/?redirect=https://cpq.huawei.com/isales/cpq/index/#/',
    }
    login_data = {
        'actionFlag': 'loginAuthenticate',
        'lang': 'en',
        'loginMethod': 'login',
        'loginPageType': 'mix',
        'redirect': None,
        'redirect_local': None,
        'redirect_modify': None,
        'scanedFinPrint': None,
        'uid': username,
        'password': password,
        'verifyCode': '2345'
    }
    URL1 = 'https://login.huawei.com/login/login.do'
    resultB = session.post(URL1, headers=header1, data=login_data, verify=False)

    return session


class iAuth:

    def __init__(self, session):

        self.session = session
        self.userAccount = ""

    def get_user(self, user_id):

        print("\nSearching User... \n\n")
        header = {
            "Host": "w3.huawei.com",
            "Referer": "http://w3.huawei.com/iauth/",
            "x-app-id": "app_0000000000014082",
            "x-sub-app-id": "grant"
        }

        URL = f"""http://w3.huawei.com/iauth/zuul/app_0000000000014082:commonservices/iauth/commonservice/services/jalor/security/user/suggest?userCN={user_id}&scope=&lang=EN"""
        resp = self.session.get(URL, headers=header, verify=False)

        if resp.status_code == 200:

            resp_dict = json.loads(resp.text)

            URL2 = f"""http://w3.huawei.com/iauth/zuul/app_0000000000014082:integration/iauth/integration/services/idm/integration/myRoleService/findMyExistRoleList/page/list/100/1?userAccount={user_id}"""
            resp2 = self.session.get(URL2, headers=header, verify=False)
            resp_dict2 = json.loads(resp2.text)

            if len(resp_dict2['result']) != 0:
                if resp_dict2['result'][0]['userAccount'] is not None:
                    self.userAccount = resp_dict2['result'][0]['userAccount']
                    print("User ID: " + resp_dict[0]['userCN'] + " Found! ✓")
            else:

                self.userAccount = resp_dict[0]['userAccount']
                print("User ID: " + resp_dict[0]['userCN'] + " Found! ✓")

        elif resp.status_code == 204:

            print("User ID not found ✘ \nPlease re-enter the correct User ID.")

            clear_download_folder()

            time.sleep(9999)

    def export_privilege(self):

        header = {
            "Host": "w3.huawei.com",
            "Referer": "http://w3.huawei.com/iauth/",
        }

        URL = f"""http://w3.huawei.com/iauth/zuul/app_0000000000014082:integration/iauth/integration/services/idm/integration/myRoleService/export?exportType=all&UserAccount={self.userAccount}&x-app-id=app_0000000000014082&x-sub-app-id=grant"""
        resp = self.session.get(URL, headers=header, verify=False)
        resp_dict = json.loads(resp.text)

        if resp_dict['result'] == "success":
            print("\n Successfully exported\n")

    def search_files(self):

        resp_dict = None
        flag_tip = True

        while flag_tip:

            try:

                header = {
                    "Host": "w3.huawei.com",
                    "Referer": "http://w3.huawei.com/iauth/",
                    "x-app-id": "app_0000000000014082",
                    "x-sub-app-id": "grant"
                }

                URL = f"""http://w3.huawei.com/iauth/zuul/app_0000000000014082:commonservices/iauth/commonservice/services/idm/commonservice/excelTask/export/list/page/50/1?fileName=&moduleName=&exportFlag="""
                resp = self.session.get(URL, headers=header, verify=False)
                resp_dict = json.loads(resp.text)


                flag_result = self.checkExportStatus(dict=resp_dict, itemName="exportFlag")

                if flag_result:
                    flag_tip = True
                    print('\n')
                    print("Waiting...")
                    for _ in range(5):
                        for sym in syms:
                            sys.stdout.write("\b%s" % sym)
                            sys.stdout.flush()
                            time.sleep(0.25)
                else:
                    flag_tip = False
                    break

            except Exception:
                print(traceback.format_exc())

        return resp_dict

    def download_file(self, resp_dict):

        task_list = []
        delete_list = []

        header = {
            "Host": "w3.huawei.com",
            "Referer": "http://w3.huawei.com/iauth/"
        }

        if resp_dict is not None:
            for results in resp_dict['result']:
                if results['moduleName'] == "Privilege":
                    task_list.append({"taskId": results['taskId'], "fileName": results['fileName']})
                    delete_list.append(results)

        for task in task_list:
            URL = f"""http://w3.huawei.com/iauth/zuul/app_0000000000014082:integration/iauth/integration/servlet/download?dlType=Excel&excelId={task['taskId']}&execFlag=EXP&exceFlag=EXPx-app-id=app_0000000000014082&x-sub-app-id=integration"""
            resp = self.session.get(URL, headers=header, verify=False)

            write_data(resp=resp, result_dir=get_working_path() + "\\download\\", filename=task['fileName'])

        return delete_list

    def delete_file(self, delete_list):

        header = {
            "Host": "w3.huawei.com",
            "Referer": "http://w3.huawei.com/iauth/",
            "x-app-id": "app_0000000000014082",
            "x-sub-app-id": "grant"
        }

        body = delete_list

        URL = "http://w3.huawei.com/iauth/zuul/app_0000000000014082:commonservices/iauth/commonservice/services/idm/commonservice/excelTask/export/d/list"

        resp = self.session.post(URL, headers=header, json=body, verify=False)

        resp_dict = self.search_files()

    def checkExportStatus(self, dict, itemName):
        """
        Check the status of the file if it is success
        :param res_dict:
        :return: True/False
        """

        check_list = []

        for items in dict['result']:
            check_list.append(items[itemName])

        check_list = set(check_list)

        # 0 = Pending, 1 = Progressing
        if "0" in check_list or "1" in check_list:
            check_list.clear()
            return True
        # 2 = Success/Completed
        else:
            check_list.clear()
            return False
