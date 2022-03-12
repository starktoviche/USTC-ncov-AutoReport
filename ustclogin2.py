from bs4 import BeautifulSoup
import requests
import numpy as np
from urllib.parse import unquote
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
class Login:
    def __init__(self, stuid, password, service):
        self.stuid=stuid
        self.password=password
        self.service=service
    
    def passport(self):
        data=self.session.get('https://passport.ustc.edu.cn/login?service='+self.service,headers=headers)
        data=data.text
        data = data.encode('ascii','ignore').decode('utf-8','ignore')
        soup = BeautifulSoup(data, 'html.parser')
        CAS_LT = soup.find("input", {"name": "CAS_LT"})['value']
        data = {
            'model': 'uplogin.jsp',
            'service': unquote(self.service),
            'warn': '',
            'showCode': '0',
            'username': self.stuid,
            'password': str(self.password),
            'button': '',
            'CAS_LT':CAS_LT,
            'LT':''
        }
        post=self.session.post('https://passport.ustc.edu.cn/login', data=data,headers=headers)
        return post
        
    def login(self):
        self.session=requests.Session()
        loginsuccess = False
        retrycount = 5
        while (not loginsuccess) and retrycount:
            result=self.passport()
            self.cookies = self.session.cookies
            retrycount = retrycount - 1
            if result.url=='https://passport.ustc.edu.cn/login':
                print("Login Failed! Retry...")
            else:
                print("Login Successful!")
                loginsuccess = True
        return loginsuccess
