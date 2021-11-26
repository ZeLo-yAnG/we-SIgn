// pages/cam/cam.js
var url
var app = getApp()
Page({

    /**
     * 页面的初始数据
     */
    data: {
        imgList: [], // 图片集合     
        baseImg: [], // base64图片集合     
        maxImg: 1, // 图片上传最高数量（根据需求设置） 
    },
    takePhoto() {
      const that = this
      const ctx = wx.createCameraContext()
      ctx.takePhoto({
        quality: 'high',
        success: (res) => {
          this.setData({
            src: res.tempImagePath
          })
          console.log(res.tempImagePath)
          wx.getFileSystemManager().readFile({
            filePath: res.tempImagePath,
            encoding: 'base64',
            success: result => {
              let src = result.data.replace(/^data:image\/\w+;base64,/, "");
              app.globalData.face = src
            }
          })
        }
      })
    },
    pushPhoto(){
      const cid = this.data.cid
      console.log(cid)
      wx.navigateTo({
        url: '/pages/sucess/sucess?sid=' + app.globalData.openid + '&cid=' + cid+'&position=' + this.data.position+'&mode='+'1',
      })
    },
    error(e) {
      console.log(e.detail)
    },


    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
      this.setData({
        cid: options.cid,
        mode: options.mode,
        position: options.position
      })

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