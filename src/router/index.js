import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import RegisterView from  '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import ExplorePage from '../views/ExplorePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../views/AboutView.vue')
      component: AboutView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/posts/new',
      name: 'newpost',
      component: () => import('../views/AddPost.vue')
    },
    {
<<<<<<< HEAD
      path:'/users/profile',
      name: 'userprofile',
      component: () => import('../views/MyProfile.vue')
    },
    {
      path: '/explore',
      name: 'explore',
      component: ExplorePage
    },
=======
      path: '/explore',
      name: 'Explore',
      component: ExplorePage
    }
>>>>>>> 3c6bd7368499e0fc031d3459f82491c18ca241a1
  ]
})

export default router
