import SignIn
import flask
import Course
import WeSignDB
import Teacher
import Student
import json
import requests

app = flask.Flask(__name__)


# 1 查询教师课程列表
@app.route("/tea/getCourseList")
def getTCourseList():
    try:
        Tid = flask.request.args.get("tid")
        teacher = Teacher.Teacher(Tid)
        return teacher.getCourseList()  # 已json格式化
    except Exception as err:
        return repr(err)


# 2 查询教师历史签到列表
@app.route("/tea/getSignList")
def getSignList():
    try:
        Cid = flask.request.args.get("cid")
        db = WeSignDB.WeSignDB()
        rows = db.select_teacher_course_signtime(Cid)
        rows = [{"time": x[0]} for x in rows]
        return json.dumps(rows)  # 已json格式化
    except Exception as err:
        return repr(err)


# 3 教师查询某次签到的学生签到记录
@app.route("/tea/getSignRecord")
def getSignRecord():
    try:
        Cid = flask.request.args.get("cid")
        Date = flask.request.args.get("date")
        db = WeSignDB.WeSignDB()
        rows = db.teacher_select_history_course_info(Cid, Date)
        sign = []
        noSign = []
        for row in rows:
            if row[2] == '0':
                noSign.append({"name": row[0], "no": row[1], "time": row[3]})
            else:
                sign.append({"name": row[0], "no": row[1], "time": row[3]})
        return json.dumps({"signed": sign, "noSign": noSign}, ensure_ascii=False)  # 已json格式化
    except Exception as err:
        return repr(err)


# 4 查询学生课堂列表
@app.route("/stu/getCourseList")
def getsCourseList():
    try:
        Sid = flask.request.args.get("sid")
        db = WeSignDB.WeSignDB()
        rows = db.select_student_course(Sid)
        rows = [{'name': x[0], 'cid': x[1]} for x in rows]
        return json.dumps(rows, ensure_ascii=False)  # 已json格式化
    except Exception as err:
        return repr(err)


# 5 查询学生签到记录
@app.route("/stu/getSignInfo")
def getSign():
    try:
        Sid = flask.request.args.get("sid")
        Cid = flask.request.args.get("cid")
        db = WeSignDB.WeSignDB()
        rows = db.select_sign_up_info(Sid, Cid)
        rows = [{"state": "未签到" if x[0] == '0' else '已签到', "time": x[1]} for x in rows]
        return json.dumps(rows, ensure_ascii=False)  # 已json格式化
    except Exception as err:
        return repr(err)


# 6 教师创建课堂
@app.route("/tea/creatCourse")
def creatCourse():
    try:
        Tid = flask.request.args.get("tid")
        name = flask.request.args.get("coursename")
        teacher = Teacher.Teacher(Tid)
        cid = teacher.createCourse(name)
        return json.dumps({"name": name, "cid": cid}, ensure_ascii=False)  # 已json格式化
    except Exception as err:
        return repr(err)


# 7 教师创建签到
@app.route("/tea/creatSign")
def addSign():
    try:
        Cid = flask.request.args.get("cid")
        mode = flask.request.args.get("mode")
        position = flask.request.args.get("position")
        position = eval("[{}]".format(position))
        if mode is not None:
            mode = list(eval("(" + mode + ")"))
        cs = Course.Course(Cid)
        res = cs.createSignIn(mode, position)
        return str(res)
    except Exception as err:
        return str(err)


# 8,12,13 学生加入课堂
@app.route("/stu/joinCourse")
def stu_addCourse():
    try:
        Sid = flask.request.args.get("sid")
        Cid = flask.request.args.get("cid")
        stu = Student.Student(Sid)
        return stu.addCourse(Cid)
    except Exception as err:
        return repr(err)


# 9 学生修改/初次填写个人信息,学号姓名
@app.route("/stu/setStuInfo")
def setStuInfo():
    try:
        Sid = flask.request.args.get("sid")
        name = flask.request.args.get("name")
        no = flask.request.args.get("no")
        stu = Student.Student(Sid)
        res = stu.setInfo(name, no)
        return str(res)
    except Exception as err:
        return repr(err)


# 10 学生签到
@app.route("/stu/doSign", methods=["GET", "POST"])
def doSign():
    try:
        Cid = flask.request.args.get("cid")
        Sid = flask.request.args.get("sid")
        face = flask.request.data.decode()
        face = json.loads(face).get('face')  # pic是图片的base64编码字符串
        position = flask.request.args.get("position")
        sign = SignIn.SignIn(Cid)
        res = sign.signIn(Sid, face, position)
        return str(res)
    except Exception as err:
        return str(err)


# 11 判断签到进行中
@app.route("/tea/getSignState")
def getSignState():
    try:
        Cid = flask.request.args.get("cid")
        sn = SignIn.SignIn(Cid)
        return sn.getState()
    except Exception as err:
        return str(err)


# 12 见8
# 13 见8
# 14 人脸是否存在
@app.route("/stu/existFace")
def existFace():
    try:
        Sid = flask.request.args.get("sid")
        stu = Student.Student(Sid)
        return str(stu.existFace())
    except Exception as err:
        return repr(err)


# 15 签到获取人脸照片

# 结束签到
@app.route("/tea/endSign")
def endSign():
    try:
        Cid = flask.request.args.get("cid")
        sn = SignIn.SignIn(Cid)
        sn.endSignIn()
        return "success end"
    except Exception as err:
        return repr(err)


# 获取学生学号姓名
@app.route("/stu/getStuInfo")
def getStuInfo():
    try:
        Sid = flask.request.args.get("sid")
        stu = Student.Student(Sid)
        return stu.getInfo()
    except Exception as err:
        return repr(err)


# 加入教师表
@app.route("/tea/insertTeaInfo")
def insertTeaInfo():
    try:
        Tid = flask.request.args.get("tid")
        Tea = Teacher.Teacher(Tid)
        res = Tea.creatTea()
        return str(res)
    except Exception as err:
        return repr(err)


# 教师获取实时签到状态
@app.route("/tea/getNowSign")
def getNowSign():
    try:
        cid = flask.request.args.get("cid")
        sn = SignIn.SignIn(cid)
        hasSign = sn.getSign()
        notSign = sn.getNoSign()
        res = {"signed": hasSign, "noSign": notSign}
        return json.dumps(res, ensure_ascii=False)
    except Exception as err:
        return repr(err)


# # 补签
# @app.route("/tea/supplement")
# def sup():
#     try:
#         cid = flask.request.args.get("cid")
#         sid = flask.request.args.get("sid")
#         sign = signList[cid]
#         res = sign.supplement(sid)
#         return str(res)
#     except Exception as err:
#         return repr(err)


# 登录返回openid
@app.route("/login")
def login():
    try:
        code = flask.request.args.get("code")
        appid = "小程序的APPID"
        secert = "密钥"
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secert + '&js_code=' + code + '&grant_type=authorization_code'
        req = requests.get(url)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        data = json.loads(req.text)
        return data['openid']
    except Exception as err:
        return repr(err)


# 上传人脸照片
@app.route("/stu/upLoadFace")
def upLoadFace():
    try:
        fileid = flask.request.args.get("fileid")
        sid = flask.request.args.get("sid")
        stu = Student.Student(sid)
        return str(stu.setFace(fileid))
    except Exception as err:
        return repr(err)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
