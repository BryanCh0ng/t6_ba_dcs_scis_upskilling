<template>
  <div>
    <button @click=runCourseAction(course.course_ID) class="btn btn-blue-green hop-on text-light font-weight-bold text-nowrap" v-if="status == 'Active'">Hop On</button>
    <button class="btn btn-warning shoutout text-light font-weight-bold text-nowrap" v-else-if="status == 'Vote'">Shout Out</button>
    <button class="btn btn-edit edit text-light font-weight-bold text-nowrap" v-else-if="status == 'Edit'">Edit</button>
    <button @click=runCourseAction(course.course_ID) class="btn btn-danger retire text-light font-weight-bold text-nowrap" v-else-if="status == 'Retire'">Retire</button>
    <button @click=runCourseAction(course.course_ID) class="btn btn-deactivate deactivate text-light font-weight-bold text-nowrap" v-else-if="status == 'Deactivate'">Deactivate</button>
    <button @click=runCourseAction(course.course_ID) class="w-100 btn btn-activate activate text-light font-weight-bold text-nowrap" v-else-if="status == 'Activate'">Activate</button>
    <button class="btn btn-activate approve text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_approve'">Approve</button>
    <button class="btn btn-danger reject text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_reject'">Reject</button>
    <button class="btn btn-info open_for_voting text-light font-weight-bold text-nowrap" v-else-if="status == 'Approved'">Open for Voting</button>
    <button class="btn btn-danger close text-light font-weight-bold text-nowrap" v-else-if="status == 'Close'">Close</button>
    <button class="btn btn-success open_for_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'Open for Registration'">Open for Registration</button>
    <button class="btn btn-primary open_for_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'Open for Voting'">Open for Voting</button>
  </div>
  
</template>

<script>
import RegistrationService from "@/api/services/RegistrationService.js"
import { axiosClient } from "@/api/axiosClient";

export default {
  props: {
    status: String,
    course: Object
  },
  data() {
    return {
      message: '',
      showModal: false,
      user_ID: ''
    };
  },
  methods: {
    closeModal() {
      this.showModal = false;
    },

    async get_user_id() {
      try {
        const user_ID = await axiosClient.get("/login/get_user_id")
        this.user_ID = user_ID.data

      } catch (error) {
        this.message = error.message
        this.user_ID = null;
      }
    },

    async runCourseAction() {
      try {
        // let response;
        if (this.status == 'Active') {
          // response = await regservice
          this.get_user_id();
          const response = await RegistrationService.createNewRegistration(this.course.rcourse_ID, this.user_ID, "Enrolled");
          this.message = response.message;
        }
        this.$emit('action-and-message-updated', {message: this.message, course: this.course});
      } catch (error) {
        console.log(error);
        this.message = error.message;
        this.$emit('action-and-message-updated', {message: this.message, course: this.course});
      }
    }
  }
};
</script>