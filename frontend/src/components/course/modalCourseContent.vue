<template>
  <div class="modal-content">
    <div class="modal-header">
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body pt-1"> 
      <div class="modal-title pt-3">
        <h5>{{ course.course_Name }}
          <course-category-badge :category="course.coursecat_Name" class="align-items-center modal-course-cat"></course-category-badge>
        </h5>
      </div>
      <div>{{ course.course_Desc }}</div>
      <div v-if="isRunCourse">
        <div class="pt-4 row">
          <div class="col-6"> 
            Course Start Date: <br> <strong>{{ convertDate(course.run_Startdate) }}</strong>
          </div>
          <div class="col-6">
            Course Start Time: <br> <strong>{{ convertTime(course.run_Starttime) }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Course End Date: <br> <strong>{{ convertDate(course.run_Enddate) }}</strong>
          </div>
          <div class="col-6">
            Course End Time: <br> <strong>{{ convertTime(course.run_Endtime) }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Course Venue: <br> <strong>{{ course.course_Venue }}</strong>
          </div>
          <div class="col-6">
            Course Format: <br> <strong>{{ course.course_Format }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Available Slots: <br> <strong>{{ course.course_Size }}</strong>
          </div>
          <div class="col-6">
            Min Slots: <br> <strong>{{ course.course_Minsize }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Fee: <br> <strong>${{ course.course_Fee }}</strong>
          </div>
          <div v-if="userRole == 'Admin'" class="col-6"> 
            Registration Count: <br> <strong>{{ course.registration_count }}</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import courseCategoryBadge from './courseCategoryBadge.vue';
import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'
import UserService from "@/api/services/UserService.js";

export default {
  components: {
    courseCategoryBadge
  },
  props: {
    course: Object
  },
  computed: {
    isRunCourse() {
      var runStatus = this.course['runcourse_Status'];
      return runStatus !== undefined
    },
    userRole() {
      return this.getUserRole()
    }
  },
  methods: {
    convertDate, 
    convertTime,
    async getUserRole() {
      try {
        const user_Role = await UserService.getUserRole()
        return user_Role
      } catch (error) {
        return null
      }
    }
  }
};
</script>