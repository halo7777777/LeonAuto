import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import AdminHome from '../views/Admin/AdminHome'
import UserHome from '../views/User/UserHome'
import Welcome from "../views/Welcome"
import Account from "../views/Admin/Account"
import Card from "../views/Admin/Card"

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: "/login"
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/AdminHome',
    name: 'AdminHome',
    component: AdminHome,
    redirect: "/welcome",
    children:[
      {path: "/welcome", component: Welcome},
      {path: "/account", component: Account},
      {path: "/tec/card", component: Card},
    ],
    meta:{requireAdmin: true}
  },
  {
    path: '/UserHome',
    name: 'UserHome',
    component: UserHome,
    meta:{requireUser: true}
  }
]

const router = new VueRouter({
  routes
})

export default router
