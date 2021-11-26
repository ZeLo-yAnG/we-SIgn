// pages/first/first.js
var app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
      haveOpenID: false
    },
    goinfor:function(){
        wx.navigateTo({
          url: '/pages/infor/infor',
        })
    },

    gosclass:function(){
      wx.navigateTo({
        url: '/pages/sclass/sclass',
      })
  },

    gotclass:function(){
        wx.navigateTo({
          url: '/pages/tclass/tclass',
        })
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
      wx.showLoading({
        title: '登录中',
      });
      var that = this
      wx.login({
        success: function (res) {
          if (res.code) {
            console.log(res)
            wx.cloud.callContainer({
              path: '/login?code='+res.code, // 填入业务自定义路径
              header: {
                'X-WX-SERVICE': 'test2', // 填入服务名称
              },
              method: 'GET',
              config: {
                env: 'wecheck01-2g88ztd3f391b60b',
              },
            }).then(res => {
              wx.hideLoading()
              console.log(res.data)
              app.globalData = {
                openid: res.data,
                haveOpenID: true
              }
              that.setData({
                haveOpenID: true
              })
            })
          } else {
            console.log('获取用户登录态失败！' + res.errMsg)
          }
        }
      });
      
    },

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