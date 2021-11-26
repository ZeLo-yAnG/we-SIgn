// pages/sucess/sucess.js
var util = require('../utils/utils.js');
var app=getApp()
Page({
    data :{
      state: "中"
    },
    onLoad: function (options) {
        // 调用函数时，传入new Date()参数，返回值是日期和时间
        var currenTime= util.formatTime(new Date());
        // 再通过setData更改Page()里面的data，动态更新页面的数据
        this.setData({
          currenTime: currenTime
        });
        
        this.setData({
          cid: options.cid,
          position: options.position,
          mode: options.mode
        });
        var that = this;
        wx.showLoading({
          title: '签到中',
        })
        if(this.data.mode=="0"){
          wx.cloud.callContainer({
            path: '/stu/doSign?sid='+app.globalData.openid+'&cid='+that.data.cid+'&position='+that.data.position, // 填入业务自定义路径
            header: {
              'X-WX-SERVICE': 'test2', // 填入服务名称
            },
            method: 'GET',
            config: {
              env: 'wecheck01-2g88ztd3f391b60b',
            },
          }).then(res=>{
            console.log(res)
            wx.hideLoading()
            if(res.data== 'True'){
              console.log("ture? "+res.data== true)
              that.setData({
                state:"成功"
              })
              
            }else{
              that.setData({
                state:"失败"
              })
            }
            
            })
        } else{
          wx.request({
            url: '{myurl}/stu/doSign?sid=' + app.globalData.openid + '&cid=' + this.data.cid+'&position='+this.data.position, // 填入业务自定义路径
            header: {
              'content-type': 'application/json', // 填入服务名称
            },
            method: 'POST',
            data: {
              face: app.globalData.face
            },
            success(res) {
              wx.hideLoading()
              console.log(res)
              if (res.data == "True") {
                that.setData({
                  state: "成功"
                })
              }else{
                that.setData({
                  state:"失败"
                })
              }
            }
          })
        }

     
          
      },
    gosclass:function(){
      wx.redirectTo({
        url: '/pages/shclass/shclass?cid='+ this.data.cid,
      })
    }

})