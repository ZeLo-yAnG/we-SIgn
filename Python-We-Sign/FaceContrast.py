# encoding:utf-8
import base64
import sqlite3
import requests

'''
人脸对比
'''


class ApiCenterClient:
    def __init__(self):
        self.host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=2zUXzOnSWl72LEeiOED4Rq4W&client_secret=密钥'
        self.request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
        self.access_token = self.getak()
        self.headers = {'content-type': 'application/json'}

    def getak(self):
        response = requests.get(self.host)
        if response:
            return response.json()['access_token']

    def facect(self, img0, img1):
        #  img0: 学生存档的照片
        #  img1: 签到时照片
        params = [{'image': img0, 'image_type': 'BASE64', 'face_type': "LIVE", 'quality_control': "LOW"},
                  {'image': img1, 'image_type': "BASE64", 'face_type': "IDCARD", 'quality_control': "LOW",
                   "liveness_control": "NORMAL"}]
        request_url = self.request_url + "?access_token=" + self.access_token
        response = requests.post(request_url, json=params, headers=self.headers)
        # print(response.json())
        if response:
            if response.json()['error_code'] == 0:
                score = response.json()['result']['score']
                return score > 70
            else:
                return False
        return False
