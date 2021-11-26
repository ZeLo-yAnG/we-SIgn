// pages/sclass/sclass.js
const app=getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
      showUploadTip: false,
      haveCreateCollection: false
    },

    goweiqian:function(){
        wx.navigateTo({
          url: '/pages/weiqian/weiqian',
        })
    },
    goinfor:function(){
      wx.navigateTo({
        url: '/pages/infor/infor',
      })
  },

    // goshclass:function(){
    //     wx.navigateTo({
    //       url: '/pages/shclass/shclass',
    //     })
    // },

    goshclass:function(e){
      const cid = e.currentTarget.id
      console.log('/pages/shclass/shclass?cid='+ cid)
        wx.navigateTo({
          url: '/pages/shclass/shclass?cid='+ cid,
        })
  },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
     
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
     wx.cloud.callContainer({
        path: '/stu/getCourseList?sid='+app.globalData.openid, // 填入业务自定义路径
        header: {
          'X-WX-SERVICE': 'test2', // 填入服务名称
        },
        method: 'GET',
        config: {
          env: 'wecheck01-2g88ztd3f391b60b',
        },
      }).then(res=>{
        this.setData({powerList: res.data})
        }
      )
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