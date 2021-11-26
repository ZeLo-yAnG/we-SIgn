// miniprogram/pages/shclass/shclass.js
const QQMapWX = require('../utils/qqmap-wx-jssdk.min');
const app = getApp()
var CID
var lat
var lon
var mode
Page({

  /**
   * 页面的初始数据
   */
  data: {
    state: false,
  },

  gocam: function () {

  },
  gosign: function () {
    const cid = this.data.cid
    console.log('/pages/shclass/shclass?sid=' + app.globalData.openid + '&cid=' + cid)
    if(mode == "[2]" || mode == "None"){
      console.log(this.data.latitude)
      wx.navigateTo({
        url: '/pages/sucess/sucess?sid=' + app.globalData.openid + '&cid=' + cid+'&position=' + this.data.longitude + ',' + this.data.latitude+'&mode='+'0',
      })
    } else {
      wx.navigateTo({
        url: '/pages/cam/cam?sid=' + app.globalData.openid + '&cid=' + cid+'&position=' + this.data.longitude + ',' + this.data.latitude+'&mode='+'1',
      })
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      cid: options.cid
    });
    this.getPosition()
    CID = options.cid
    var that = this;
    wx.cloud.callContainer({
      path: '/stu/getSignInfo?sid=' + app.globalData.openid + '&cid=' + that.data.cid, // 填入业务自定义路径
      header: {
        'X-WX-SERVICE': 'test2', // 填入服务名称
      },
      method: 'GET',
      config: {
        env: 'wecheck01-2g88ztd3f391b60b',
      },
    }).then(res => {
      this.setData({
        powerList: res.data
      })
    })
    wx.cloud.callContainer({
      path: '/tea/getSignState?cid=' + that.data.cid, // 填入业务自定义路径
      header: {
        'X-WX-SERVICE': 'test2', // 填入服务名称
      },
      method: 'GET',
      config: {
        env: 'wecheck01-2g88ztd3f391b60b',
      },
    }).then(res => {
      console.log(res)
      this.setData({
        state: res.data.state
      })
      if (res.data.state == true) {
        mode = res.data.mode
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  getPosition: function(){
    let that = this;
    // 引入腾讯地图
    let qqmapsdk = new QQMapWX({
      key: 'UULBZ-JZVC3-ALH3Y-YHYS7-GPAZO-ZQFM7' // 必填
    });
    // 使用 wx.createMapContext 获取 map 上下文
    that.mapCtx = wx.createMapContext('myMap');
    wx.getLocation({
      // 国内只能使用gcj02坐标系，wgs84不能使用；高德地图等都是使用的gcj02
      type: "gcj02",
      success: function (res) {
        that.setData({
          latitude: res.latitude,
          longitude: res.longitude
        })
        console.log(res.latitude, res.longitude)
      }

    })
  },


  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },
})