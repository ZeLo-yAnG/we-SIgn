// pages/weiqian/weiqian.js
const app=getApp()
Page({
  
    /**
     * 页面的初始数据
     */
    data: {
    },
    getcid: function (e) {
      this.setData({
        Cid: e.detail.value
      })
    },
    gosclass:function(){
        wx.navigateTo({
          url: '/pages/sclass/sclass',
        })
    },
    resetData: function () {
      console.log('/stu/joinCourse?cid='+this.data.Cid+"&sid="+app.globalData.openid)
      wx.cloud.callContainer({
        path: '/stu/joinCourse?cid='+this.data.Cid+"&sid="+app.globalData.openid, // 填入业务自定义路径
        header: {
          'X-WX-SERVICE': 'test2', // 填入服务名称
        },
        method: 'GET',
        config: {
          env: 'wecheck01-2g88ztd3f391b60b',
        },
      }).then(res=>{
        console.log(res)
        var tips = res.data
        if(res.data == 'success'){
          tips = '加入成功'
        }
        wx.navigateTo({
          url: '/pages/signsucess/signsucess?state='+tips,
        })
      })
    },
})