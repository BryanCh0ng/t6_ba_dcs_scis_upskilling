<template>
  <div class="full-screen-container" id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <nav-bar v-if="showNavBar"/>
    <div class="content">
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
      const routesWithNavBar = ["ContactUs", "viewCourse","adminViewRunCourse", "adminViewVoteCourse", "adminViewProposedCourse","adminVotingCampaign", "adminViewInstructorsTrainers", "studentViewCourse", "instructorTrainerViewProfile"];
      return routesWithNavBar.includes(this.$route.name);
    }
  }
};
</script>