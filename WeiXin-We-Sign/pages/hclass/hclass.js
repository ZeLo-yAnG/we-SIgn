// pages/hclass/hclass.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    state: false
  },
  goNowSign: function(e){
    wx.navigateTo({
      url: '/pages/thclass/thclass?cid='+ this.data.cid,
    }) 
    console.log("go now sign"+ '/pages/thclass/thclass?cid='+ this.data.cid)
  },
  newSign: function (e) {
    wx.navigateTo({
      url: '/pages/newsign/newsign?cid=' + this.data.cid,
    })
  },

  gothclass: function (e) {
      const time = e.currentTarget.id
      console.log('/pages/historySign/historySign?time='+ encodeURI(time)+'&cid='+this.data.cid)
        wx.navigateTo({
          url: '/pages/historySign/historySign?time='+ encodeURI(time)+'&cid='+this.data.cid,
        })
    },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      cid: options.cid
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
    var that = this
    console.log(app.globalData)
    wx.cloud.callContainer({
      path: '/tea/getSignList?cid='+that.data.cid, // 填入业务自定义路径
      header: {
        'X-WX-SERVICE': 'test2', // 填入服务名称
      },
      method: 'GET',
      config: {
        env: 'wecheck01-2g88ztd3f391b60b',
      },
    }).then(res => {
      console.log(res)
      that.setData({
        powerList: res.data
      })
    })

    wx.cloud.callContainer({
      path: '/tea/getSignState?cid='+that.data.cid, // 填入业务自定义路径
      header: {
        'X-WX-SERVICE': 'test2', // 填入服务名称
      },
      method: 'GET',
      config: {
        env: 'wecheck01-2g88ztd3f391b60b',
      },
    }).then(res => {
      console.log(res.data)
      that.setData({
        state: res.data.state
      })
    })
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