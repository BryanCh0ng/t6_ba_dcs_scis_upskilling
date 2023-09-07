<template>
  <div>
    <button class="btn btn-warning shoutout text-light font-weight-bold text-nowrap" v-if="status == 'Vote'">Shout Out</button>
    <button class="btn btn-edit edit text-light font-weight-bold text-nowrap" v-else-if="status == 'Edit'">Edit</button>
    <button @click="runCourseAction(course.course_ID)" class="btn btn-danger retire text-light font-weight-bold text-nowrap w-100" v-else-if="status == 'Retire'">Retire</button>
    <button @click="runCourseAction(course.course_ID)" class="btn btn-deactivate deactivate text-light font-weight-bold text-nowrap" v-else-if="status == 'Deactivate'">Deactivate</button>
    <button @click="runCourseAction(course.course_ID)" class="w-100 btn btn-activate activate text-light font-weight-bold text-nowrap" v-else-if="status == 'Activate'">Activate</button>
    <button @click=runCourseAction(course.course_ID) class="btn btn-blue-green hop-on text-light font-weight-bold text-nowrap" v-if="status == 'Active'">Hop On</button>
    <button class="btn btn-activate approve text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_approve'">Approve</button>
    <button class="btn btn-danger reject text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_reject'">Reject</button>
    <button class="btn btn-info open_for_voting text-light font-weight-bold text-nowrap" v-else-if="status == 'Approved'">Open for Voting</button>
    <button class="btn btn-danger close text-light font-weight-bold text-nowrap" v-else-if="status == 'Close'">Close</button>
    <button class="btn btn-success promote_to_course text-light font-weight-bold text-nowrap" v-else-if="status == 'promote_to_course'">Promote to course</button>
    <button class="btn btn-primary open_for_voting text-light font-weight-bold text-nowrap" v-else-if="status == 'open_for_voting'">Open for Voting</button>
    <button class="btn btn-danger close text-light font-weight-bold text-nowrap" v-else-if="status == 'proposed_delete'">Delete</button>
    <button class="btn btn-success open_for_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'open_for_registration'">Open for Registeration</button>
    <button class="btn btn-danger close_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'close_registration'">Close registration</button>  
    <button class="btn btn-success create_run text-light font-weight-bold text-nowrap" v-else-if="status == 'create_run'">Create Run</button> 
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
  