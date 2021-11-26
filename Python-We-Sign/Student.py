import WeSignDB
import json


class Student:
    def __init__(self, sid):
        self.id = sid
        self.db = WeSignDB.WeSignDB()

    # 学生是否存在
    def existStu(self):
        self.db.cursor.execute("SELECT EXISTS(SELECT * FROM Student WHERE wStudentID =%s)", self.id)
        exist = self.db.cursor.fetchone()[0]  # 0:不存在 1：存在
        return exist

    # 添加学生
    def creatStu(self, name, no):
        self.db.insert_Student(self.id, name, no)
        return True

    # 修改个人信息
    def setInfo(self, name, Sno):
        if self.existStu() == 1:
            self.db.update_student_name(self.id, name)
            self.db.update_student_no(self.id, Sno)
        else:
            self.creatStu(name, Sno)
        return True

    # 获取个人信息
    def getInfo(self):
        if self.existStu() == 1:
            res = self.db.select_student_info(self.id)
            return json.dumps({"name": res[0], "NO": res[1]}, ensure_ascii=False)
        else:
            return "未填写姓名学号"

    # 获取加入的课程
    def getCourse(self):
        return self.db.select_student_course(self.id)

    # 获取某课程的签到记录
    def getHistory(self, CID):
        return self.db.select_sign_up_info(self.id, CID)

    #  学生加入课程
    def addCourse(self, CID):
        if self.db is None:
            self.db = WeSignDB.WeSignDB()
        if self.existStu() == 0:
            return "未填写姓名学号"
        stateCode = self.db.insert_SC(self.id, CID)
        if stateCode == 1:
            self.db.cmommit()
            return "success"
        elif stateCode == -1:
            return "课程码错误"
        else:
            return "未知错误"

    # 判断人脸是否存在，存在返回True
    def existFace(self):
        self.db.cursor.execute("SELECT wFace FROM `Student` where wstudentid = %s", self.id)
        res = self.db.cursor.fetchone()[0]
        if res is None:
            return False
        else:
            return True

    # 修改/上传人脸照片
    def setFace(self, face_file_id):
        self.db.cursor.execute("UPDATE Student SET wFace=%s WHERE wStudentID=%s", (face_file_id, self.id))
        return True
