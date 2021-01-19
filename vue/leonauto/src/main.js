import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './plugins/element.js'
import  './assets/font/iconfont.css'   // 引入iconfont
import './assets/css/global.css'
import instance from'./http.js'

Vue.prototype.$http = instance

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


  if(!AdminToken && to.meta.requireAdmin === true)
  {
    next({path: from.fullPath})
  }

  if(!UserToken && to.meta.requireUser === true)
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
    console.log(777)
    // 未登录
    next('/login')
  }
  else
  {
    next()
  }
})