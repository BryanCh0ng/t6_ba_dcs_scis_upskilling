<template>
  <div class="full-screen-container" id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <nav-bar v-if="showNavBar" class="mb-5"/>
    <div>
      <router-view />
    </div>
  </div>
</template>

<script>
import NavBar from "./components/common/NavBar.vue";

export default {
  name: "App",
  components: {
    NavBar,
  },
  computed: {
    showNavBar() {
      // Specify the routes where you want to show the navbar
      const routesWithNavBar = ["ContactUs", "viewCourse","adminViewRunCourse", "adminViewVoteCourse", "adminViewProposedCourse","adminVotingCampaign", "adminViewInstructorsTrainers", "studentViewCourse","studentViewProfile", "editProposedCourse", "instructorTrainerViewProfile","proposeCourse", "editCourse", "createCourse", "createRunCourse", "editRunCourse", "instructorTrainerViewVotingCampaign", "adminViewCourse", "studentViewRecommendations", "adminViewManagement", "adminViewStudentEnrolledCourse", "adminAddAdmin", "adminViewCourseRun", "viewDashboard", "viewCourseFeedbackAnalysis", "viewRunCourseFeedbackAnalysis", "viewInstructorFeedbackAnalysis", "createFeedbackTemplate", "editFeedbackTemplate" ,"adminViewFeedbackTemplate", "submitFeedback", "viewAllLessons", "viewRunCourseLesson", "viewRunCourseLesson", "createRunCourseLesson", "editRunCourseLesson", "viewAttendance", "adminViewRegistration", "studentViewLesson", "instructorTrainerViewLesson"];
      return routesWithNavBar.includes(this.$route.name);
    }
  }
};
</script>