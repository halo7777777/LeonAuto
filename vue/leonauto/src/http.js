import axios from 'axios' // 导入axios跨域
import { Message } from 'element-ui'
import router from './router'

var instance = axios.create({timeout: 1000*12})
instance.defaults.baseURL = "http://localhost:9090"   // 设置访问根路径 后端路径

// http request 拦截器
instance.interceptors.request.use(
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
instance.interceptors.response.use(
    response => {
      return response;
    },
    error => {
      if(error.response){
        console.log(error.response.data);
        switch(error.response.data.errno){
          case 118:
            // 返回118 清除token信息并跳转到登录页面
            sessionStorage.clear() 
            router.replace({
              path: '/login',
              query: {redirect: router.currentRoute.fullPath}   // 重新登录后，返回之前的页面
            })
            Message({showClose:true, message:'未登录，返回登陆界面', type:'error', duration:3000})  
     
        }
      }
      return Promise.resolve(error.response);  // 返回接口的错误信息
    }
  )
  
export default instance