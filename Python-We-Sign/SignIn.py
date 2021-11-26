import base64
import json
import requests
import WeSignDB
import PositionContrast
from FaceContrast import ApiCenterClient


class SignIn:
    def __init__(self, CourseID, mode=None, position=None):
        self.CourseID = CourseID
        self.anti_cheating_Mode = mode  # 反作弊功能,1:人脸识别, 2:定位, demo:[1,2]
        self.DB = WeSignDB.WeSignDB()
        self.position = position
        self.data = self.DB.getCdata(self.CourseID)

    # 对每个学生进行签到
    def signIn(self, stuID, face=None, position=None):
        """
        :param stuID: 学生ID
        :param face: 签到时人脸照片的路径
        :param position: 经纬度信息 [,]
        :return: 签到结果
        """
        state = True
        data = self.data
        # print(data)
        if not data[1] == 'None':
            mode = eval(data[1])
            if 1 in mode:  # 人脸识别
                if face == '':
                    return False
                self.faceContrast = ApiCenterClient()
                self.faceContrast.getak()
                appid = ""
                secert = ""
                url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secert
                req = requests.get(url)
                req.raise_for_status()
                req.encoding = req.apparent_encoding
                self.AccessToken = json.loads(req.text)['access_token']
                img0 = self.get_face(stuID)
                stateFace = self.faceContrast.facect(img0, face)
                if not stateFace:
                    state = stateFace
            if 2 in mode:  # 定位
                self.position = eval(data[2])
                position = eval('[' + position + ']')
                # position = eval(position)
                statePoi = PositionContrast.PositionContrast(self.position[0], self.position[1], position[0],
                                                             position[1], 100)
                if not statePoi:
                    state = statePoi
        if state:
            self.DB.insert_Sign(self.CourseID, data[0], stuID, '1')
            self.DB.cmommit()
        return state

    # 获取数据库里的人脸图像base64编码
    def get_face(self, stuID):
        file_id = self.DB.select_student_face_info(stuID)[0]
        # print("file_id:", file_id)
        data = {
            "env": "wecheck01-2g88ztd3f391b60b",
            "file_list": [
                {
                    "fileid": file_id,
                    "max_age": 1200
                }
            ]
        }
        html = requests.post("https://api.weixin.qq.com/tcb/batchdownloadfile?access_token=" + self.AccessToken,
                             json=data)
        html = json.loads(html.text)
        download_url = html['file_list'][0]['download_url']
        # print('download_url: ', download_url)
        pic = requests.get(download_url)
        img0 = pic.content
        img0 = base64.b64encode(img0).decode()
        return img0

    # 签到进行状态
    def getState(self):
        State = self.DB.getCdata(self.CourseID)
        # print(State)
        if State[3] == '1':
            return json.dumps({"state": True, "mode": str(State[1])}, ensure_ascii=False)
        else:
            return json.dumps({"state": False})

    # 创建签到
    def createSignIn(self):
        self.DB.cursor.execute("SELECT SignState FROM Course WHERE wCourseID = %s", self.CourseID)
        exist = self.DB.cursor.fetchone()[0]
        if exist != '1':
            self.DB.update_SignState(self.CourseID, '1', str(self.anti_cheating_Mode), str(self.position))
        return True

    # 获取已签到表
    def getSign(self):
        self.DB.cursor.execute("SELECT wNo, wName FROM Sign,Student "
                               "WHERE Sign.wStudentID = Student.wStudentID "
                               "AND wCourseID = %s AND wDate = %s"
                               , (self.CourseID, self.data[0]))
        res_Signed = self.DB.cursor.fetchall()
        signed = [{"no": x[0], "name": x[1]} for x in res_Signed]
        return signed

    # 获取未签到学生
    def getNoSign(self):
        self.DB.cursor.execute("SELECT wNo, wName,wStudentID FROM Student WHERE wStudentID IN"
                               "(SELECT wStudentID FROM SC WHERE wCourseID =%s AND wStudentID NOT in ("
                               "SELECT wStudentID FROM Sign WHERE wCourseID=%s AND wDate = %s))"
                               , (self.CourseID, self.CourseID, self.data[0]))
        res_NoSigned = self.DB.cursor.fetchall()
        noSign = [{"no": x[0], "name": x[1], "sid": x[2]} for x in res_NoSigned]
        return noSign

    # 结束签到，将结果存入数据库，0：未签到，1：已签到
    def endSignIn(self):
        noSign = self.getNoSign()
        for s in noSign:
            self.DB.insert_Sign(self.CourseID, self.data[0], s['sid'], '0')
        self.DB.cursor.execute("UPDATE Course set SignState='0' WHERE wCourseID=%s", self.CourseID)
        self.DB.closeDB()

    # 补签
    # def supplement(self, stuID):
    #     self.DB.insert_Sign(self.CourseID, self.date, stuID, '1')
    #     self.DB.cmommit()
    #     return True

    def teacher_getHistoryRecord(self, date):
        return self.DB.teacher_select_history_course_info(self.CourseID, date)


if __name__ == '__main__':
    # sn = SignIn('1')

    # print(sn.getSign())
    # print(sn.getNoSign())
    # sn.endSignIn()
    # test = SignIn('1', mode=[1])
    # img1 = open(r'C:/Users/YZL/Desktop/1.jpg', 'rb')
    # img1 = base64.b64encode(img1.read()).decode()
    # print(test.signIn('12', face=img1))
    # test.endSignIn()
    sn = SignIn('3')
    print((sn.signIn("oLVqt5CuWLVwdf-Uct-U-vZsTHto")))
    # print(sn.signIn('12', position='119.19575942469022, 26.05859794496616'))
