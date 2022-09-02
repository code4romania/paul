import Vue from 'vue'
import VueRouter from 'vue-router'
import TokenService from '../services/storage'

import Base from '@/views/Base'
import Page404 from '@/views/404'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: {
      name: 'login'
    }
  },
  {
    path: '/account',
    name: 'account',
    component: () =>
      import(/* webpackChunkName: "account" */ '@/views/AccountBase.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () =>
          import(/* webpackChunkName: "account" */ '@/views/AccountLogin.vue'),
        meta: {
          public: true,
          anonymousOnly: true
        }
      },
      {
        path: 'register',
        name: 'register',
        component: () =>
          import(
            /* webpackChunkName: "account" */ '@/views/AccountRegister.vue'
          ),
        meta: {
          public: true,
          anonymousOnly: true
        }
      },
      {
        path: 'activate/:uid/:token',
        name: 'activate',
        component: () =>
          import(
            /* webpackChunkName: "account" */ '@/views/AccountActivate.vue'
          ),
        meta: {
          public: true,
          anonymousOnly: true
        }
      },
      {
        path: 'forgot-password',
        name: 'forgot-password',
        component: () =>
          import(
            /* webpackChunkName: "account" */ '@/views/AccountForgotPass.vue'
          ),
        meta: {
          public: true,
          anonymousOnly: true
        }
      },
      {
        path: 'reset-password/:uid/:token',
        name: 'reset-password',
        component: () =>
          import(
            /* webpackChunkName: "account" */ '@/views/AccountResetPass.vue'
          ),
        meta: {
          public: true,
          anonymousOnly: true
        }
      }
    ]
  },
  {
    path: '/app',
    name: 'app',
    component: Base,
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () =>
          import(/* webpackChunkName: "dashboard" */ '@/views/Dashboard.vue')
      },
      {
        path: 'database',
        name: 'database-view',
        component: () =>
          import(/* webpackChunkName: "database" */ '@/views/DatabaseView.vue')
      },
      {
        path: 'edit-data',
        name: 'edit-data',
        component: () =>
          import(/* webpackChunkName: "database" */ '@/views/DatabaseView.vue')
      },
      {
        path: 'table/:idTable',
        name: 'table-view',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableView.vue')
      },
      {
        path: 'table-add/',
        name: 'table-add',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableAdd.vue')
      },
      {
        path: 'table-edit/:idTable?',
        name: 'table-edit',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableEdit.vue')
      },
      {
        path: 'table/:idTable/entity/:idEntity',
        name: 'entity-view',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableEntityView.vue')
      },
      {
        path: 'table-import',
        name: 'table-import',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableImportForm.vue')
      },
      {
        path: 'table-import-edit/:idTable',
        name: 'table-import-edit',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableImportEdit.vue')
      },
      {
        path: 'table-import-result/:idImport',
        name: 'table-import-result',
        component: () =>
          import(
            /* webpackChunkName: "table" */ '@/views/TableImportResult.vue'
          )
      },
      {
        path: 'table/:idTable/entity-edit/:idEntity?',
        name: 'entity-edit',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableEntityEdit.vue')
      },
      {
        path: 'filter-views',
        name: 'filter-view',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/FilterView.vue')
      },
      {
        path: 'filter-table/:idTable',
        name: 'filter-table-view',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/TableView.vue'),
        props: {
          filterMode: true
        }
      },
      {
        path: 'filter-edit/:idTable?',
        name: 'filter-edit',
        component: () =>
          import(/* webpackChunkName: "table" */ '@/views/FilterEdit.vue')
      },
      {
        path: 'charts/',
        name: 'charts-view',
        component: () =>
          import(/* webpackChunkName: "chart" */ '@/views/ChartsView.vue')
      },
      {
        path: 'chart/:idChart',
        name: 'chart-view',
        component: () =>
          import(/* webpackChunkName: "chart" */ '@/views/ChartView.vue')
      },
      {
        path: 'chart-edit/:idChart?',
        name: 'chart-edit',
        component: () =>
          import(/* webpackChunkName: "chart" */ '@/views/ChartEdit.vue')
      },
      {
        path: 'cards/',
        name: 'cards-view',
        component: () =>
          import(/* webpackChunkName: "chart" */ '@/views/CardsView.vue')
      },
      {
        path: 'card/:idCard',
        name: 'card-view',
        component: () =>
          import(/* webpackChunkName: "chart" */ '@/views/CardView.vue')
      },
      {
        path: 'card-edit/:idCard?',
        name: 'card-edit',
        component: () =>
          import(/* webpackChunkName: "chart" */ '@/views/CardEdit.vue')
      },
      {
        path: 'users',
        name: 'users-view',
        component: () =>
          import(/* webpackChunkName: "user" */ '@/views/Users.vue')
      },
      {
        path: 'users/:idUser',
        name: 'user-profile',
        component: () =>
          import(/* webpackChunkName: "user" */ '@/views/UserProfile.vue')
      },
      {
        path: 'users/:idUser/change-password',
        name: 'change-password',
        component: () =>
          import(/* webpackChunkName: "user" */ '@/views/UserChangePass.vue')
      },
      {
        path: 'plugin/:plugin',
        name: 'plugin-view',
        component: () =>
          import(/* webpackChunkName: "plugin" */ '@/views/PluginView.vue')
      },
      {
        path: 'plugin/:plugin/task/:idTask',
        name: 'plugin-task-view',
        component: () =>
          import(/* webpackChunkName: "plugin" */ '@/views/PluginTaskView.vue')
      },
      {
        path: 'plugin/:plugin/task-edit/:idTask?',
        name: 'plugin-task-edit',
        component: () =>
          import(/* webpackChunkName: "plugin" */ '@/views/PluginTaskEdit.vue')
      },
      { path: '*', component: Page404 }
    ]
  },
  { path: '*', component: Page404 }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const isPublic = to.matched.some(record => record.meta.public)
  const anonymousOnly = to.matched.some(record => record.meta.anonymousOnly)
  const isLoggedIn = !!TokenService.getToken()

  if (!isPublic && !isLoggedIn) {
    return next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
  }

  if (isLoggedIn && anonymousOnly) {
    return next('/app/dashboard')
  }

  next()
})

export default router
