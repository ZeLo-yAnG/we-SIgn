import pymysql
import pymysql.err

class WeSignDB:
    def __init__(self):
        self.con = pymysql.connect(host="", port=, user="root", passwd="", db="wesign",
                                   charset="utf8", autocommit=True)
        self.cursor = self.con.cursor()

        # 创建微签数据库所使用的表
        try:
            # 创建Student表
            self.cursor.execute(
                'create table IF NOT EXISTS Student(wStudentID varchar(255) unique ,wName varchar(255) NOT NULL ,wNo varchar(255) NOT NULL ,wFace varchar (255), '
                'primary key (wStudentID))')
            # 创建教师表
            self.cursor.execute(
                'create table  IF NOT EXISTS Teacher(wTeacherID varchar(255) unique , primary key (wTeacherID))')
            # 创建课程表
            self.cursor.execute(
                'create table  IF NOT EXISTS Course(wCourseID varchar (255) unique ,wCourseName varchar (255),wTeacherID varchar (255),'
                'primary key (wCourseID),foreign key (wTeacherID) references Teacher(wTeacherID))')
            # 创建选修表关系表
            self.cursor.execute(
                'create table  IF NOT EXISTS SC(wStudentID varchar (255), wCourseID varchar (255),primary key (wStudentID,wCourseID),'
                'foreign key(wStudentID) references Student(wStudentID),foreign key (wCourseID) references Course(wCourseID))')
            # 创建签到表
            self.cursor.execute(
                'create table  IF NOT EXISTS Sign(wCourseID varchar (255),wDate DATETIME,wStudentID varchar (255),wState varchar (255), signInTime TIME,'
                'primary key (wCourseID,wStudentID,wDate),foreign key (wStudentID) references Student(wStudentID))')
        except Exception as err:
            print(err)

    # 更新数据
    def cmommit(self):
        self.con.commit()

    # 关闭数据库
    def closeDB(self):
        self.con.commit()
        self.con.close()

    # 插入数据:
    # 向Student表插入数据
    def insert_Student(self, StudentID, Name, No):
        try:
            self.cursor.execute("insert into Student(wStudentID,wName,wNo) values (%s,%s,%s)",
                                (StudentID, Name, No))
        except Exception as err:
            print(err)

    # 获取mode和position
    def getCdata(self, CourseID):
        try:
            self.cursor.execute(
                "select DATE_FORMAT(SignTime,'%%y-%%m-%%d %%H:%%i:%%S'),mode,position,SignState from Course where wCourseID = %s",
                CourseID)
            return self.cursor.fetchone()
        except Exception as err:
            print(err)

    # 向教师表插入数据
    def insert_Teacher(self, TeacherID):
        try:
            self.cursor.execute('insert into Teacher(wTeacherID) values (%s)',
                                (TeacherID))
        except Exception as err:
            print(err)

    # 向选修关系表插入数据
    def insert_SC(self, StudentID, CourseID):
        try:
            self.cursor.execute("insert into SC(wStudentID,wCourseID) values (%s,%s)",
                                (StudentID, CourseID))
            return 1

        except pymysql.err.IntegrityError:
            return -1

        except Exception:
            return 0

    # 向Course表更新Sign数据
    def update_SignState(self, CourseID, SignState, Mode=None, Position=None):
        try:
            self.cursor.execute(
                "update Course set SignState = %s,mode = %s,position = %s,SignTime = now() "
                "where wCourseID = %s", (SignState, Mode, Position, CourseID))
        except Exception as err:
            print(err)

    # 向签到关系表插入数据
    def insert_Sign(self, CourseID, date, StudentID, State):
        try:
            self.cursor.execute(
                "insert into Sign(wCourseID,wDate,wStudentId,wState,signintime) values (%s, %s,%s,%s,CURRENT_TIME())",
                (CourseID, date, StudentID, State))
        except Exception as err:
            print(err)

    # 向课程关系表插入数据
    def insert_Course(self, CourseID, CourseName, TeacherID):
        try:
            self.cursor.execute("insert into Course(wCourseID,wCourseName,wTeacherID) values (%s,%s,%s)",
                                (CourseID, CourseName, TeacherID))
        except Exception as err:
            print(err)

    ###查询数据

    # 学生查询自身信息
    def select_student_info(self, StudentID):
        try:
            self.cursor.execute("select wName,wNo from Student "
                                "where wStudentID = %s", StudentID)
            return self.cursor.fetchone()
        # fetchall()返回结果类似如下:[(0, 0, u'name1'), (1, 0, u'hello')]
        except Exception as err:
            print(err)

    # 查询学生已经加入的课程
    def select_student_course(self, StudentID):
        try:
            self.cursor.execute("select wCourseName, wCourseID from Course "
                                "where wCourseID in "
                                "(select wCourseID from SC "
                                "where wStudentID = %s)", StudentID)
            return self.cursor.fetchall()
        except Exception as err:
            print(err)

    # 查询选修该课程的所有学生信息
    def select_studentID_by_courseID(self, CourseID):
        try:
            self.cursor.execute("select wStudentID from SC "
                                "where wCourseID = %s", CourseID)
            return self.cursor.fetchall()
        except Exception as err:
            print(err)

    # 查询教师教授的课程创建的签到时间
    def select_teacher_course_signtime(self, CourseID):
        try:
            self.cursor.execute("SELECT DATE_FORMAT(wDate,'%%y-%%m-%%d %%H:%%i:%%S')"
                                " FROM Sign WHERE wCourseID = %s"
                                " GROUP BY wDate"
                                " ORDER BY wDate DESC", CourseID)
            return self.cursor.fetchall()
        except Exception as err:
            print(err)

    # 查询学生存入的人脸识别信息
    def select_student_face_info(self, StudentID):
        try:
            self.cursor.execute("select wFace from Student "
                                "where wStudentID = %s", StudentID)
            return self.cursor.fetchone()
        except Exception as err:
            print(err)

    # 查询课程号对应的课程名
    def select_coursename(self, CourseID):
        try:
            self.cursor.execute("select wCourseName from Course "
                                "where wCourseID = %s", CourseID)
            return self.cursor.fetchall()
        except Exception as err:
            print(err)

    # 查询历史签到信息,返回签到时间，签到状态
    def select_sign_up_info(self, StudentID, CourseID):
        try:
            # self.select_coursename(CourseID)
            self.cursor.execute("select wState,DATE_FORMAT(wDate,'%%y-%%m-%%d %%H:%%i:%%S') from Sign "
                                "where wStudentID = %s "
                                "and wCourseID = %s"
                                " order by wDate desc ", (StudentID, CourseID))
            return self.cursor.fetchall()
        except Exception as err:
            print(err)

    # 教师查看课程列表
    def select_teacher_course(self, TeacherID):
        try:
            self.cursor.execute("select wCourseID, wCourseName from Course"
                                " where wTeacherID = %s", TeacherID)
            return self.cursor.fetchall()
        except Exception as err:
            print(err)

    # 教师端查询历史课堂签到状态
    def teacher_select_history_course_info(self, CourseID, Date):
        try:
            self.cursor.execute("SELECT wName,wNo,wState,TIME_FORMAT(signInTime,'%%H:%%i:%%S')"
                                " FROM Sign,Student"
                                " WHERE wCourseID = %s and wDate = %s"
                                " AND Student.wStudentID = Sign.wStudentID", (CourseID, Date))
            return self.cursor.fetchall()
        except Exception as err:
            print(err)

    ###修改数据库信息
    # 修改学生姓名
    def update_student_name(self, StudentID, New_Name):
        try:
            self.cursor.execute("update Student set wName = %s"
                                "where wStudentID = %s", (New_Name, StudentID))

        except Exception as err:
            print(err)

    # 修改学生学号
    def update_student_no(self, StudentID, New_No):
        try:
            self.cursor.execute("update Student set wNo = %s"
                                "where wStudentID = %s", (New_No, StudentID))

        except Exception as err:
            print(err)


# 删除信息


##测试
# if __name__ == '__main__':
    # db = WeSignDB()

    # print(a)
    # db.createDB()
    # a = db.teacher_select_history_course_info('1', '2021-11-14 20:50:21')
    # print(a)
    # db.insert_Student('1','ly','2','12312')
    # db.insert_Teacher('1')
    # db.insert_Course('2','操作系统','1')
    # db.insert_SC('1','2')
    # db.insert_Sign('1','11.3','1','未签到')
    # print(db.select_student_info('1'))
    # print(db.select_student_face_info('1'))
    # print(db.select_sign_up_info('1','1'))
    # print((db.select_coursename('2')))
    # print(db.select_student_course('1'))
    # print(db.select_studentID_from_courseID('2'))
    # b.update_student_no('1','3')
    # db.closeDB()


# db = WeSignDB()
