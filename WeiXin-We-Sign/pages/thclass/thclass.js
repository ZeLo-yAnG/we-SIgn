// miniprogram/pages/thclass/thclass.js
const app = getApp()
let interval = null;
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
  endSign: function () {
    console.log('endsign /tea/endSign?cid=' + this.data.cid)
    wx.cloud.callContainer({
      path: '/tea/endSign?cid=' + this.data.cid, // 填入业务自定义路径
      header: {
        'X-WX-SERVICE': 'test2', // 填入服务名称
      },
      method: 'GET',
      config: {
        env: 'wecheck01-2g88ztd3f391b60b',
      },
    }).then(res => {
      console.log("end sign" + res.data)
      clearInterval(interval)
      wx.navigateBack({
        delta: 2,
      })
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      cid: options.cid
    })
    interval = setInterval(this.getNowSign, 30000)
  },

  onHide: function () {
    clearInterval(interval)
  },

  onUnload: function () {
    clearInterval(interval)
  },

  getNowSign: function(){
    var that = this
    console.log("签到统计" +'/tea/getNowSign?cid=' + this.data.cid)
    wx.cloud.callContainer({
      path: '/tea/getNowSign?cid=' + that.data.cid, // 填入业务自定义路径
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
  onShow: function(options){
    this.getNowSign()
  },
  onUnload: function(){
    wx.redirectTo({
      url: '/pages/hclass/hclass?cid='+ this.data.cid ,
    })
  }
})