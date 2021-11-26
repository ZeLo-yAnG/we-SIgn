// pages/infor/infor.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    sid: "",
    name: ""
  },
  getsid: function (e) {
    this.setData({
      sid: e.detail.value,

    })
  },
  getname: function (e) {
    this.setData({
      name: e.detail.value,
    })
  },
  gosclass: function () {
    wx.navigateTo({
      url: '/pages/sclass/sclass',
    })
  },
  gocam1: function () {
    wx.navigateTo({
      url: '/pages/cam1/cam1',
    })
  },
  resetData: function () {
    console.log('/stu/setStuInfo?sid=' + app.globalData.openid + '&no=' + this.data.sid + "&name=" + encodeURI(this.data.name))
    if (this.data.sid != '' && this.data.name != '') {
      wx.cloud.callContainer({
        path: '/stu/setStuInfo?sid=' + app.globalData.openid + '&no=' + this.data.sid + "&name=" + encodeURI(this.data.name), // 填入业务自定义路径
        header: {
          'X-WX-SERVICE': 'test2', // 填入服务名称
        },
        method: 'GET',
        config: {
          env: 'wecheck01-2g88ztd3f391b60b',
        },
      }).then(res => {
        console.log(res)
        console.log("非空，name:(" + encodeURI(this.data.name) + ")no:(" + this.data.sid + ")")
        wx.showToast({
          title: "修改成功",
          icon: "success",
          duration: 2000,
          success: function () {
            wx.navigateBack({
              delta: 1,
            })
          }
        })
      })
    } else {
      console.log("空")
      wx.showToast({
        title: "学号姓名不能为空",
        icon: "none",
        duration: 2000
      })
    }
  },


  /**
   * 生命周期函数--监听页面加载
   */

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})