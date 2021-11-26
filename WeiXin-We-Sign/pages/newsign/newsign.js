// pages/newsign/newsign.js
const QQMapWX = require('../utils/qqmap-wx-jssdk.min');
Page({

  /**
   * 页面的初始数据
   */
  data: {
    mode: '',
    position: false,
    havePos: false,
    items: [{
        opt: '1',
        name: '人脸识别'
      },
      {
        opt: '2',
        name: '定位'
      }
    ]
  },
  checkboxChange: function (e) {
    var mymode = ''
    var items = e.detail.value
    console.log(items)
    this.setData({
      position: false
    })
    for (var i in items) {
      mymode = mymode + items[i] + ','
      if (items[i] == "2") {
        this.setData({
          position: true
        })
      }
    }
    this.setData({
      mode: mymode
    })
    console.log(this.data)
  },

  gothclass: function () {
    var parms = '/tea/creatSign?cid=' + this.data.cid
    if (this.data.mode != '') {
      parms = parms + '&mode=' + this.data.mode
    }
    if (this.data.position) {
      parms = parms + '&position=' + this.data.longitude + ',' + this.data.latitude
    }
    console.log(parms)
    wx.cloud.callContainer({
      path: parms, // 填入业务自定义路径
      header: {
        'X-WX-SERVICE': 'test2', // 填入服务名称
      },
      method: 'GET',
      config: {
        env: 'wecheck01-2g88ztd3f391b60b',
      },
    }).then(res => {
      console.log(res)
      wx.navigateTo({
        url: '/pages/thclass/thclass?cid=' + this.data.cid,
      })
    })
  },
  getcid: function (e) {
    this.setData({
      cid: e.detail.value
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options.cid)
    this.setData({
      cid: options.cid
    })
    this.getPosition()
  },
  getPosition: function () {
    wx.showLoading({
        title: '获取位置信息中',
      })
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
          longitude: res.longitude,
          havePos: true
        })
        console.log(res.latitude, res.longitude)
         wx.hideLoading()
      }

    })
  },

})