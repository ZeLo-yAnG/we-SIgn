// miniprogram/pages/thclass/thclass.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    sign: true,
    nosign: false,
    realTime: null
  },
  haveSigned: function () {
    this.setData({
      sign: true,
      nosign: false
    })
  },
  noSigned: function () {
    this.setData({
      nosign: true,
      sign: false
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      time: options.time,
      cid: options.cid
    })
    this.getSignRecord()
  },

  onHide: function () {
    clearInterval(this.interval)
  },

  onUnload: function () {
    clearInterval(this.interval)
  },

  getSignRecord: function(){
    var that = this
    console.log("签到统计" +'/tea/getSignRecord?cid=' + this.data.cid+'&date='+this.data.time)
    wx.cloud.callContainer({
      path:'/tea/getSignRecord?cid=' + this.data.cid+'&date='+this.data.time, // 填入业务自定义路径
      header: {
        'X-WX-SERVICE': 'test2', // 填入服务名称
      },
      method: 'GET',
      config: {
        env: 'wecheck01-2g88ztd3f391b60b',
      },
    }).then(res => {
      // console.log(res)
      that.setData({
        powerList: res.data
      })
      console.log(res)
    })
  },
  onUnload: function(){
    wx.redirectTo({
      url: '/pages/hclass/hclass?cid='+ this.data.cid ,
    })
  }
})