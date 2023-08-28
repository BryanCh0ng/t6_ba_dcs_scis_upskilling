<template>
  <button class="btn btn-blue-green hop-on text-light font-weight-bold text-nowrap" v-if="status == 'Active'">Hop On</button>
  <button class="btn btn-warning shoutout text-light font-weight-bold text-nowrap" v-else-if="status == 'Vote'">Shout Out</button>
  <button class="btn btn-edit edit text-light font-weight-bold text-nowrap" v-else-if="status == 'Edit'">Edit</button>
  <button @click=deleteRunCourse(id) class="btn btn-danger delete text-light font-weight-bold text-nowrap" v-else-if="status == 'Delete'">Delete</button>
  <button class="btn btn-deactivate deactivate text-light font-weight-bold text-nowrap" v-else-if="status == 'Deactivate'">Deactivate</button>
  <button class="btn btn-activate activate text-light font-weight-bold text-nowrap" v-else-if="status == 'Activate'">Activate</button>
  <button class="btn btn-activate approve text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_approve'">Approve</button>
  <button class="btn btn-danger reject text-light font-weight-bold text-nowrap" v-else-if="status == 'pending_reject'">Reject</button>
  <button class="btn btn-info open_for_voting text-light font-weight-bold text-nowrap" v-else-if="status == 'Approved'">Open for Voting</button>
  <button class="btn btn-danger close text-light font-weight-bold text-nowrap" v-else-if="status == 'Close'">Close</button>
  <button class="btn btn-success open_for_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'Open for Registration'">Open for Registration</button>
  <button class="btn btn-primary open_for_registration text-light font-weight-bold text-nowrap" v-else-if="status == 'Open for Voting'">Open for Voting</button>
  <div v-else-if="status == 'Pending'"></div>
</template>

<script>

import CourseService from "@/api/services/CourseService.js"


export default {
  props: {
    status: String,
    id: Number
  },
  methods: {
    async deleteRunCourse(ID) {

      try {
          let response
          response = await CourseService.deleteRunCourse(ID); // Use the CourseService
          alert(response.message)
          } 
      catch (error) {
        console.log(error)
        alert(error)
      }
    },
  }
};
</script>
  