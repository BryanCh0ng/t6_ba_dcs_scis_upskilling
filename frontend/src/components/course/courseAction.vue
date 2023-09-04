<template>
  <div>
    <button class="btn btn-warning shoutout text-light font-weight-bold text-nowrap" v-if="status == 'Vote'">Shout Out</button>
    <button class="btn btn-edit edit text-light font-weight-bold text-nowrap" v-else-if="status == 'Edit'">Edit</button>
    <button @click="runCourseAction(course.course_ID)" class="btn btn-danger retire text-light font-weight-bold text-nowrap" v-else-if="status == 'Retire'">Retire</button>
    <button @click="runCourseAction(course.course_ID)" class="btn btn-deactivate deactivate text-light font-weight-bold text-nowrap" v-else-if="status == 'Deactivate'">Deactivate</button>
    <button @click="runCourseAction(course.course_ID)" class="w-100 btn btn-activate activate text-light font-weight-bold text-nowrap" v-else-if="status == 'Activate'">Activate</button>
    <button @click=runCourseAction(course.course_ID) class="btn btn-blue-green hop-on text-light font-weight-bold text-nowrap" v-if="status == 'Active'">Hop On</button>
    <button class="btn btn-activate approve text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_approve'">Approve</button>
    <button class="btn btn-danger reject text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_reject'">Reject</button>
    <button class="btn btn-info open_for_voting text-light font-weight-bold text-nowrap" v-else-if="status == 'Approved'">Open for Voting</button>
    <button class="btn btn-danger close text-light font-weight-bold text-nowrap" v-else-if="status == 'Close'">Close</button>
    <button class="btn btn-success open_for_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'Open for Registration'">Open for Registration</button>
    <button class="btn btn-primary open_for_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'Open for Voting'">Open for Voting</button>
    <button class="btn btn-success attendance-list text-light font-weight-bold text-nowrap" v-else-if="status == 'attendance'">Attendance List</button>
    <button class="btn btn-success feedback-analysis text-light font-weight-bold text-nowrap" v-else-if="status == 'feedback-analysis'">Feedback Analysis</button>
    <button class="btn btn-danger proposed_delete text-light font-weight-bold text-nowrap" v-else-if="status == 'proposed_delete'">Delete</button> 
    <button class="btn btn-danger registered_drop text-light font-weight-bold text-nowrap" v-else-if="status == 'registered_drop'">Drop</button>
    <button class="btn btn-warning say_pass text-light font-weight-bold text-nowrap" v-else-if="status == 'say_pass'">Say pass</button> 
    <button class="btn btn-success provide_feedback text-light font-weight-bold text-nowrap" v-else-if="status == 'provide_feedback'">Provide Feedback</button>
    </div>
</template>
  
<script>
import CourseService from "@/api/services/CourseService.js"
import RegistrationService from "@/api/services/RegistrationService.js"
import UserService from "@/api/services/UserService.js";

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
    async runCourseAction() {
      try {
        let response;
        if (this.status == 'Retire') {
          response = await CourseService.retireRunCourse(this.course.course_ID);
        } else if (this.status == 'Activate') {
          response = await CourseService.activateRunCourse(this.course.course_ID);
        } else if (this.status == 'Deactivate') {
          response = await CourseService.deactivateRunCourse(this.course.course_ID);
        } else  if (this.status == 'Active') {
          this.get_user_id();
          response = await RegistrationService.createNewRegistration(this.course.rcourse_ID, 1, "Pending");
        }
        this.message = response.message;
        this.$emit('action-and-message-updated', {message: this.message, course: this.course});
      } catch (error) {
        this.message = error.message
        this.$emit('action-and-message-updated', {message: this.message, course: this.course});
      }
    },
      async get_user_id() {
        try {
          const user_ID = await UserService.getUserID()
          this.user_ID = user_ID

        } catch (error) {
          this.message = error.message
          this.user_ID = null;
        }
      }
  }
};
</script>
  