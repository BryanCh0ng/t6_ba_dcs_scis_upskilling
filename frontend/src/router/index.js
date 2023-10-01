import { createRouter, createWebHistory } from 'vue-router';
import UserService from "@/api/services/UserService";

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
      requiresAuth: true
    },
  },
  {
    path: '/adminViewRunCourse',
    name: 'adminViewRunCourse',
    component: () => import('../views/course/adminViewRunCourse.vue'),
    meta: {
      title: 'adminViewRunCourse',
      requiresAuth: true
    },
  },
  {
    path: '/adminViewProposedCourse',
    name: 'adminViewProposedCourse',
    component: () => import('../views/course/adminViewProposedCourse.vue'),
    meta: {
        title: 'Admin View Proposed Course',
        requiresAuth: true
    },
  },
  {
    path: '/adminViewVoteCourse',
    name: 'adminViewVoteCourse',
    component: () => import('../views/course/adminViewVoteCourse.vue'),
    meta: {
        title: 'Admin View Vote Course',
        requiresAuth: true
    },
  },
  {
    path: '/studentViewCourse',
    name: 'studentViewCourse',
    component: () => import('../views/course/studentViewCourse.vue'), 
    meta: {
        title: 'Student View Course',
        requiresAuth: true
    },
  },
  {
    path: '/studentViewRecommendations',
    name: 'studentViewRecommendations',
    component: () => import('../views/course/studentViewRecommendations.vue'),
    meta: {
        title: 'Student View Recommendations',
        requiresAuth: true
    },
  },
  {
    path: '/proposeCourse',
    name: 'proposeCourse',
    component: () => import('../views/course/ProposeCourse.vue'),
    meta: {
        title: 'Propose Course',
        requiresAuth: true
    },
  },
  {
    path: '/createCourse',
    name: 'createCourse',
    component: () => import('../views/course/CreateCourse.vue'),
    meta: {
        title: 'Create Course',
        requiresAuth: true
    },
  }, 
  {
    path: '/editCourse/:id',
    name: 'editCourse',
    component: () => import('../views/course/EditCourse.vue'),
    meta: {
        title: 'Edit Course',
        requiresAuth: true
    },
  },
  {
    path: '/createRunCourse/:id',
    name: 'createRunCourse',
    component: () => import('../views/course/CreateRunCourse.vue'),
    meta: {
        title: 'Create Run Course',
        requiresAuth: true
    },
  },
  {
    path: '/editRunCourse/:id',
    name: 'editRunCourse',
    component: () => import('../views/course/EditRunCourse.vue'),
    meta: {
        title: 'Edit Run Course',
        requiresAuth: true
    },
  },
  {
    path: '/editProposedCourse/:courseId/:action?',
    name: 'editProposedCourse',
    component: () => import('../views/course/editProposedCourse.vue'),
    meta: {
        title: 'Edit Proposed Course',
        requiresAuth: true
    },
  },    
  {
    path: '/studentViewProfile',
    name: 'studentViewProfile',
    component: () => import('../views/profile/studentViewProfile.vue'),
    meta: {
        title: 'Student View Profile',
        requiresAuth: true
    },
  },
  {
    path: '/instructorTrainerViewProfile',
    name: 'instructorTrainerViewProfile',
    component: () => import('../views/profile/instructorTrainerViewProfile.vue'),
    meta: {
        title: 'Instructor Trainer View Profile',
        requiresAuth: true
    }
  },
  {
    path: '/instructorTrainerViewVotingCampaign',
    name: 'instructorTrainerViewVotingCampaign',
    component: () => import('../views/course/instructorTrainerViewVotingCampaign.vue'),
    meta: {
        title: 'Instructor Trainer View Voting Campaign',
        requiresAuth: true
    }
  },
  {
    path: '/adminViewCourse',
    name: 'adminViewCourse',
    component: () => import('../views/course/adminViewCourse.vue'),
    meta: {
        title: 'Admin View Course',
        requiresAuth: true
    }
  },
  {
    path: '/adminViewManagement',
    name: 'adminViewManagement',
    component: () => import('../views/usermanagement/adminViewManagement.vue'),
    meta: {
        title: 'Admin View Management'
        //requiresAuth: true
    }
  },
  {
    path: '/adminViewStudentEnrolledCourse/:user_ID',
    name: 'adminViewStudentEnrolledCourse',
    component: () => import('../views/course/adminViewStudentEnrolledCourse.vue'),
    meta: {
        title: 'Admin View Student Enrolled Course',
        requiresAuth: true
    }
  },
  {
    path: '/adminAddAdmin',
    name: 'adminAddAdmin',
    component: () => import('../views/usermanagement/adminAddAdmin.vue'),
    meta: {
        title: 'Admin Add Admin'
    }
  },
  {
    path: '/adminChangePassword',
    name: 'adminChangePassword',
    component: () => import('../views/usermanagement/adminChangePassword.vue'),
    meta: {
        title: 'Admin Change Password'
    }
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

// router.beforeEach((to, _from, next) => {
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     sessionStorage.getItem("role") ? next() : next({ path: '/', });

//   } else if (to.matched.some(record => record.meta.isAuth)) {
//     sessionStorage.getItem("role") ? next({ path: '/student' }) : next();

//   } else {
//     next();
//   }
// });

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;

  if (requiresAuth) {
    try {
      const user_ID = await UserService.getUserID();
      console.log(user_ID)
      if (typeof user_ID === 'number' && user_ID > 0) {
        next();
      } else {
        next('/login');
      }
    } catch (error) {
      console.error(error);
      next(error); 
    }
  } else {
    next();
  }
});

export default router