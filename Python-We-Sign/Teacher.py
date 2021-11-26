import WeSignDB
import datetime
import random
import json


class Teacher:
    def __init__(self, Tid):
        self.TID = Tid
        self.db = WeSignDB.WeSignDB()

    # 创建一门课程
    def createCourse(self, CourseName):
        Cno = self.__getCon()
        self.db.insert_Course(Cno, CourseName, self.TID)
        self.db.cmommit()
        return Cno

    # 获取所有课程
    def getCourseList(self):
        rows = self.db.select_teacher_course(self.TID)
        courses = []
        for row in rows:
            course = {'cid': row[0], 'name': row[1]}
            courses.append(course)
        res = json.dumps(courses, ensure_ascii=False)
        return res

    # 添加教师
    def creatTea(self):
        self.db.insert_Teacher(self.TID)
        return True

    def __getCon(self):
        while True:
            CnoA = datetime.datetime.now().strftime('%d%H%M')
            CnoB = str(random.randint(0, 99))
            Cno = CnoA + CnoB
            self.db.cursor.execute("SELECT EXISTS(SELECT * FROM Course WHERE wCourseID =%s)", Cno)
            exist = self.db.cursor.fetchone()[0]
            if exist == 0:
                return Cno


# t = Teacher(1)
# t.createCourse("course1")
