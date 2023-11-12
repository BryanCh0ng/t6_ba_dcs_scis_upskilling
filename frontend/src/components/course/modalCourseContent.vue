<template>
  <div class="modal-content">
    <div class="modal-header">
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeModal"></button>
    </div>
    <div class="modal-body pt-1"> 
      <div class="modal-title pt-3">
        <div v-if="isRunCourse">
          <h5>{{ course.run_Name }}
          <course-category-badge :category="course.coursecat_Name" class="align-items-center modal-course-cat"></course-category-badge>
        </h5>
        </div>
        <div v-else>
          <h5>{{ course.course_Name }}
            <course-category-badge :category="course.coursecat_Name" class="align-items-center modal-course-cat"></course-category-badge>
          </h5>
        </div>
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
        <div class="pt-3 row">
          <div class="col-6">
            Feedback Start Date: <br> <strong>{{ convertDate(course.feedback_Startdate) }}</strong>
          </div>
          <div class="col-6">
            Feedback Start Time: <br> <strong>{{ convertTime(course.feedback_Starttime) }}</strong>
          </div>
        </div>
        <div class="pt-3 row">
          <div class="col-6">
            Feedback End Date: <br> <strong>{{ convertDate(course.feedback_Enddate) }}</strong>
          </div>
          <div class="col-6">
            Feedback End Time: <br> <strong>{{ convertTime(course.feedback_Endtime) }}</strong>
          </div>
        </div>
      </div>
      <div class="pt-5 row">
        <div class="col-12 d-flex">
          <h5 class="col-6">{{ course_rating }}</h5>
        </div>
        <div class="col-12 d-flex">
          <h5 class="col-6">Feedbacks: </h5>
        </div>
        <div v-if="feedback_reviews && feedback_reviews.length > 0">
          <div class="col-6" v-for="feedback in feedback_reviews" :key="feedback.feedback_ID">
              <p>{{ feedback.answer }}</p>
          </div>
        </div>
        <div class="row" v-else>
          <h5 class="text-center">{{ errorMessage }}</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import courseCategoryBadge from './courseCategoryBadge.vue';
import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'
import UserService from "@/api/services/UserService.js";
import FeedbackService from "@/api/services/FeedbackService.js";
import DashboardService from "@/api/services/dashboardService.js";

export default {
  components: {
    courseCategoryBadge
  },
  props: {
    course: Object,
    no_of_reviews: {
      type: Number, 
      default: 3
    }
  },
  data() {
    return {
      noOfReviews: this.no_of_reviews,
      errorMessage: "",
      feedback_reviews: {},
      course_rating: "",
      total_feedbacks: ""
    };
  },
  computed: {
    isRunCourse() {
      var runStatus = this.course['runcourse_Status'];
      console.log(this.course)
      return runStatus !== undefined
    },
    userRole() {
      return this.getUserRole()
    },
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
    },
    async getReviews() {
      this.feedback_reviews = {};
      this.course_rating = "";
      this.total_feedbacks = "";
      this.errorMessage = "";
      if (this.isRunCourse) {
       try {
        const response = await FeedbackService.getRandomReviews(this.course.rcourse_ID, null, this.noOfReviews)
        console.log(response)
        if (response.code == 200) {
          this.feedback_reviews = response.reviews
        } else {
          this.errorMessage = response.message
        } 
        let rcourse_ids = [parseInt(this.course.rcourse_ID)];
        rcourse_ids = JSON.stringify(rcourse_ids);
        const rating_response = await DashboardService.getCourseAverageRatings(null, null, rcourse_ids, null, null, null)
        if (rating_response.code == 200) {
            console.log(this.course.rcourse_ID)
            console.log(rcourse_ids)
            const no_of_feedback_response = await DashboardService.getTotalFeedbacks(null, null, rcourse_ids, null, null, null)
            console.log(no_of_feedback_response)
            if (no_of_feedback_response.code == 200) {
              this.course_rating = "Rating: " + rating_response.data.overall_average_rating + "/5 out of " + no_of_feedback_response.data.total_feedbacks + " feedback(s)";
            } 
            // else {
            //   this.errorMessage = no_of_feedback_response.message
            // }
        } else {
          this.errorMessage = rating_response.message
        }
      } catch (error) {
        console.log(error)
        //this.errorMessage = error.message
      }
      } else {
       try {
        const response = await FeedbackService.getRandomReviews(null, this.course.course_ID, this.noOfReviews)
        if (response.code == 200) {
          this.feedback_reviews = response.reviews
        } else {
          this.errorMessage = response.message
        }
        let course_ids = [parseInt(this.course.course_ID)];
        course_ids = JSON.stringify(course_ids);
        const rating_response = await DashboardService.getCourseAverageRatings(course_ids, null, null, null, null, null)
        if (rating_response.code == 200) {
          console.log(this.course.course_ID)
          console.log(course_ids)
          const no_of_feedback_response = await DashboardService.getTotalFeedbacks(course_ids, null, null, null, null, null)
          console.log(no_of_feedback_response)
          if (no_of_feedback_response.code == 200) {
            this.course_rating = "Rating: " + rating_response.data.overall_average_rating + "/5 out of " + no_of_feedback_response.data.total_feedbacks + " feedback(s)";
          } 
          // else {
          //   this.errorMessage = no_of_feedback_response.message
          // }
        } else {
          this.errorMessage = rating_response.message
        }
      } catch (error) {
        console.log(error)
        //this.errorMessage = error.message
      }
      }
    }
  },
  created() {
    // console.log('created')
    this.getReviews()
  },
  watch: {
    course: function (newVal) { 
     console.log(newVal)
    //  console.log('test')
     this.getReviews()
    }
  }
};
</script>