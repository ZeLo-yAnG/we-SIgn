import SignIn
import WeSignDB


class Course:
    start = False
    signIn = None
    db = None

    def __init__(self, CourseID):
        self.CourseID = CourseID

    #  结束签到
    def endSignIn(self):
        if self.start:
            self.signIn.endSignIn()
            self.start = False

    #  补签
    def supplementSignIn(self, StuId):
        if self.start:
            return self.signIn.supplement(StuId)

    #  创建一场签到
    def createSignIn(self, mode=None, position=None):
        sn = SignIn.SignIn(self.CourseID, mode, position)
        return sn.createSignIn()

# cou = Course('123')
# cou.addCourse('1')
# cou.startSignIn()
