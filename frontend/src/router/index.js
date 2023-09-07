import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../components/common/HelloWorld.vue'),
        meta: {
            title: 'Home',
        },
    },
    {
      path: '/blacklistfilter',
      name: 'blacklist',
      component: () => import('../components/search/BlacklistAttendanceSearchFilter.vue'),
      meta: {
          title: 'Blacklist Attendencec Search Filter',
      },
  },
  {
    path: '/commonsearchfilter',
    name: 'commonsearchfilter',
    component: () => import('../components/search/CommonSearchFilter.vue'),
    meta: {
        title: 'common search filter',
    },
  },
  {
      path: '/contactUs',
      name: 'ContactUs',
      component: () => import('../views/ContactUs.vue'),
      meta: {
          title: 'Contact Us',
      },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: {
      isAuth: true,
      title: 'Login',
    },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Registration.vue'),
    meta: {
      title: 'Register',
    },
  },
  {
    path: '/registerform',
    name: 'Register Form',
    component: () => import('../views/RegistrationForm.vue'),
    meta: {
      title: 'Register Form',
    },
  },
  {
    path: '/forgotPassword',
    name: 'ForgotPassword',
    component: () => import('../views/ForgotPassword.vue'),
    meta: {
      title: 'Forgot Password',
    },
  },
  {
    path: '/resetPassword',
    name: 'ResetPassword',
    component: () => import('../views/ResetPassword.vue'),
    meta: {
      title: 'Reset Password',
    },
  },
  {
    path: '/contactUs',
    name: 'ContactUs',
    component: () => import('../views/ContactUs.vue'),
    meta: {
      title: 'Contact Us',
    },
  },
  {
    path: '/adminViewRunCourse',
    name: 'adminViewRunCourse',
    component: () => import('../views/course/adminViewRunCourse.vue'),
    meta: {
      title: 'adminViewRunCourse',
    },
  },
  {
    path: '/adminViewProposedCourse',
    name: 'adminViewProposedCourse',
    component: () => import('../views/course/adminViewProposedCourse.vue'),
    meta: {
        title: 'Admin View Proposed Course',
    },
  },
  {
    path: '/adminViewVoteCourse',
    name: 'adminViewVoteCourse',
    component: () => import('../views/course/adminViewVoteCourse.vue'),
    meta: {
        title: 'Admin View Vote Course',
    },
  },
  {
    path: '/adminViewInstructorsTrainers',
    name: 'adminViewInstructorsTrainers',
    component: () => import('../views/course/adminViewInstructorsTrainers.vue'),
    meta: {
        title: 'Admin View Instructors Trainers',
    },
  },
  {
    path: '/studentViewCourse',
    name: 'studentViewCourse',
    component: () => import('../views/course/studentViewCourse.vue'),
    meta: {
        title: 'Student View Course',
    },
  },
  {
    path: '/studentViewRecommendations',
    name: 'studentViewRecommendations',
    component: () => import('../views/course/studentViewRecommendations.vue'),
    meta: {
        title: 'Student View Recommendations',
    },
  },
  {
    path: '/editProposedCourse/:courseId?',
    name: 'editProposedCourse',
    component: () => import('../views/course/editProposedCourse.vue'),
    meta: {
        title: 'Edit Proposed Course',
    },
  }
  // },
  // {
  //     path: '/deleteCourse',
  //     name: 'Delete Courses',
  //     component: () => import('../components/DeleteCourse.vue'),
  //     meta: {
  //         requiresAdminAuth: true,
  //         title: 'Delete Courses',
  //     },
  // },
  // {
  //     path: '/createCourse',
  //     name: 'CreateCourse',
  //     component: () => import('../views/CreateCourse.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'CreateCourseForm',
  //     },
  // },
  // {
  //     path: '/editCourse/:course_id?',
  //     name: 'EditCourseForm',
  //     component: () => import('../views/EditCourse.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'EditCourseForm',
  //     },
  // },
  // {
  //     path: '/roles',
  //     name: 'Roles',
  //     component: () => import('../views/Roles.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'Roles',
  //     },
  // },
  // {
  //     path: '/admin',
  //     name: 'HRRoles',
  //     component: () => import('../views/HRRoles.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'HRRoles',
  //     },
  // },
  // {
  //     path: '/createRole',
  //     name: 'CreateRole',
  //     component: () => import('../views/CreateRole.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'CreateRoleForm',
  //     },
  // },
  // {
  //     path: '/editRole/:role_id?',
  //     name: 'EditRole',
  //     component: () => import('../views/EditRole.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'EditRoleForm',
  //     },
  // },
  // {
  //     path: '/skills',
  //     name: 'Skills',
  //     component: () => import('../views/Skills.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'Skills',
  //     },
  // },
  // {
  //     path: '/createSkill',
  //     name: 'Create Skill',
  //     component: () => import('../views/CreateSkill.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'Create Skill',
  //     },
  // },
  // {
  //     path: '/editSkill/:skill_id?',
  //     name: 'Edit Skill',
  //     component: () => import('../views/EditSkill.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'Edit Skill',
  //     },
  // },
  // {
  //     path: '/skillCard',
  //     name: 'skillCard',
  //     component: () => import('../components/SkillCard.vue'),
  //     meta: {
  //         requiresAuth: true,
  //         title: 'skillCard',
  //     }
  // },
  // {
  //     path: '/forbidden',
  //     name: 'Forbidden',
  //     component: () => import(/* webpackChunkName: "403" */ '../views/error-403.vue'),
  //     meta: {
  //         title: 'Forbidden',
  //     },
  // },
  // {
  //     //https://stackoverflow.com/questions/63526486/vue-router-catch-all-wildcard-not-working
  //     path: '/:catchAll(.*)',
  //     name: 'NotFound',
  //     component: () => import(/* webpackChunkName: "404" */ '../views/error-404.vue'),
  //     meta: {
  //         title: 'NotFound',
  //     },
  // },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, _from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    sessionStorage.getItem("role") ? next() : next({ path: '/', });

  } else if (to.matched.some(record => record.meta.isAuth)) {
    sessionStorage.getItem("role") ? next({ path: '/student' }) : next();

  } else {
    next();
  }
});

export default router