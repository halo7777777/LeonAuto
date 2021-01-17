import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './plugins/element.js'
import  './assets/font/iconfont.css'   // 引入iconfont
import './assets/css/global.css'

import axios from 'axios' // 导入axios跨域
import { Message } from 'element-ui'


Vue.prototype.$http = axios
axios.defaults.baseURL = "http://localhost:9090"   // 设置访问根路径 后端路径
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

// 路由守护
router.beforeEach((to, from, next)=>{
  const AdminToken = window.sessionStorage.getItem('AdminToken')
  const UserToken = window.sessionStorage.getItem('UserToken')

  var accessToken = null
  if(AdminToken)
    accessToken = AdminToken
  else if(UserToken)
    accessToken = UserToken 

  if(accessToken)
  {
      if(Object.keys(from.query).length !== 0)
      {
        let redirect = from.query.redirect
        if(to.path === redirect) // 解决无限循环问题
        {
          next()
        }
        else
        {
          next({path:redirect}) // 重新登录后，转到之前的页面
        }
      }
  }


  if(!AdminToken && to.path === '/AdminHome')
  {
    next({path: from.fullPath})
  }

  if(!UserToken && to.path === '/UserHome')
  {
    next({path: from.fullPath})
  }

  if(accessToken && to.path !== '/login')
  {
    // 有token 但不是去 login页面
    next()
  }
  else if(accessToken && to.path === '/login')
  {
    //用户已经登陆，不让访问Login登录界面
    next({path: from.fullPath})
  }
  else if(!accessToken && to.path !== '/login')
  {
    // 未登录
    next('/login')
  }
  else
  {
    next()
  }
})

// http request 拦截器
axios.interceptors.request.use(
  config =>{
    if(sessionStorage.getItem("AdminToken"))
    {
        config.headers.Authorization = sessionStorage.getItem("AdminToken")
    }
    else if(sessionStorage.getItem("UserToken"))
    {
      config.headers.Authorization = sessionStorage.getItem("UserToken")
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  }
)

// http response 拦截器
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if(error.response){
      console.log('axios:' + error.response.status);
      switch(error.response.status){
        case 403:
          // 返回403 清除token信息并跳转到登录页面
          sessionStorage.clear() 
          router.replace({
            path: '/login',
            query: {redirect: router.currentRoute.fullPath}   // 重新登录后，返回之前的页面
          })
          Message({showClose:true, message:'未登录，返回登陆界面', type:'error', duration:3000})  
   
      }
    }
    return Promise.reject(error);   // 返回接口的错误信息
  }
)