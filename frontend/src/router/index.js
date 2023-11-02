import { createRouter, createWebHistory } from 'vue-router';
import UserService from "@/api/services/UserService";

const routes = [
  {
      path: '/contactUs',
      name: 'ContactUs',
      component: () => import('../views/ContactUs.vue'),
      meta: {
          title: 'Contact Us',
      },
  },
  {
    path: '/',
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
    path: '/createFeedbackTemplate',
    name: 'createFeedbackTemplate',
    component: () => import('../views/feedbackTemplate/createFeedbackTemplate.vue'),
    meta: {
        title: 'Create Feedback Template',
        requiresAuth: true
    }
  },
  {
    path: '/editFeedbackTemplate/:id',
    name: 'editFeedbackTemplate',
    component: () => import('../views/feedbackTemplate/editFeedbackTemplate.vue'),
    meta: {
        title: 'Edit Feedback Template',
        requiresAuth: true
    },
  },
  {
    path: '/adminViewFeedbackTemplate',
    name: 'adminViewFeedbackTemplate',
    component: () => import('../views/feedbackTemplate/adminViewFeedbackTemplate.vue'),
    meta: {
        title: 'Admin View Feedback Template',
        requiresAuth: true
    },
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
    path: '/createFeedbackTemplate',
    name: 'createFeedbackTemplate',
    component: () => import('../views/feedbackTemplate/createFeedbackTemplate.vue'),
    meta: {
        title: 'Create Feedback Template',
        requiresAuth: true
    }
  },
  {
    path: '/editFeedbackTemplate/:id',
    name: 'editFeedbackTemplate',
    component: () => import('../views/feedbackTemplate/editFeedbackTemplate.vue'),
    meta: {
        title: 'Edit Feedback Template',
        requiresAuth: true
    },
  },
  {
    path: '/adminViewFeedbackTemplate',
    name: 'adminViewFeedbackTemplate',
    component: () => import('../views/feedbackTemplate/adminViewFeedbackTemplate.vue'),
    meta: {
        title: 'Admin View Feedback Template',
        requiresAuth: true
    },
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
  // Need to add authentication
  {
    path: '/viewDashboard',
    name: 'viewDashboard',
    component: () => import('../views/dashboard/viewDashboard.vue'),
    meta: {
        title: 'Admin View Dashboard',
        requiresAuth: true
    }
  },
  {
    path: '/viewCourseFeedbackAnalysis/:id',
    name: 'viewCourseFeedbackAnalysis',
    component: () => import('../views/dashboard/viewDashboard.vue'),
    meta: {
        title: 'Admin View Feedback Analysis of a Particular Course',
        requiresAuth: true
    }
  },
  {
    path: '/viewRunCourseFeedbackAnalysis/:id',
    name: 'viewRunCourseFeedbackAnalysis',
    component: () => import('../views/dashboard/viewDashboard.vue'),
    meta: {
        title: 'Admin View Feedback Analysis of a Particular Run Course',
        requiresAuth: true
    }
  },
  {
    path: '/submitFeedback/:id',
    name: 'submitFeedback',
    component: () => import('../views/feedback/submitFeedback.vue'),
    meta: {
        title: 'Submit Feedback',
    },
  },
  {
    path: '/adminViewManagement',
    name: 'adminViewManagement',
    component: () => import('../views/usermanagement/adminViewManagement.vue'),
    meta: {
        title: 'Admin View Management',
        requiresAuth: true
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
        title: 'Admin Add Admin',
        requiresAuth: true
    }
  },
  {
    path: '/adminViewCourseRun/:id',
    name: 'adminViewCourseRun',
    component: () => import('../views/course/adminViewCourseRun.vue'),
    meta: {
        title: 'Submit Feedback',
        requiresAuth: true
    },
  },
  {
    path: '/viewAllLessons',
    name: 'viewAllLessons',
    component: () => import('../views/lesson/viewAllLessons.vue'),
    meta: {
        title: 'View All Lessons',
        requiresAuth: true
    },
  }, 
  {
    path: '/viewRunCourseLesson/:id',
    name: 'viewRunCourseLesson',
    component: () => import('../views/lesson/viewRunCourseLesson.vue'),
    meta: {
        title: 'View Run Course Lesson',
        requiresAuth: true
    }, 
  }, 
  {
    path: '/viewAttendance/:lessonId',
    name: 'viewAttendance',
    component: () => import('../views/attendance/viewAttendance.vue'),
    meta: {
        title: 'View Attendance',
        requiresAuth: true
    }, 
  } 
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.meta.requiresAuth;

  if (requiresAuth) {
    try {
      const user_ID = await UserService.getUserID();
      console.log(user_ID)
      if (typeof user_ID === 'number' && user_ID > 0) {
        next();
      } else {
        next('/');
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