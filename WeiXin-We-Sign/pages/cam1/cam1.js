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
          wx.cloud.uploadFile({
            cloudPath: 'StuFace/'+app.globalData.openid+'.jpg', // 上传至云端的路径
            filePath: res.tempImagePath, // 小程序临时文件路径
            config: {
              env: 'wecheck01-2g88ztd3f391b60b',
            },
            success: res => {
              // 返回文件 ID
              console.log(res.fileID)
              wx.cloud.callContainer({
                path: '/stu/upLoadFace?sid='+app.globalData.openid+'&fileid='+res.fileID, // 填入业务自定义路径
                header: {
                  'X-WX-SERVICE': 'test2', // 填入服务名称
                },
                method: 'GET',
                config: {
                  env: 'wecheck01-2g88ztd3f391b60b',
                },
              }).then(res=>{
                console.log(res)
                if(res.data== 'True'){
                  console.log("ture? "+res.data== true)
                  that.setData({
                    state:"成功"
                  })
                }
                }
              )
            },
            fail: console.error
          })
        }
      })
  },
    error(e) {
      console.log(e.detail)
    },
  back:function(){
    wx.navigateBack({
      delta: 1,
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