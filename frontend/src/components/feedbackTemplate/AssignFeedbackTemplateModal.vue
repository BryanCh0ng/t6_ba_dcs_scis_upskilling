<template>
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body pt-1"> 
        <div class="modal-title pt-3">
          <h3 class="text-center">Assign {{ feedback_template.template_Name }} To Course(s)</h3>
        </div>
        <div v-if="!error">
          <div class="row mt-5">
            <div class="col-lg-6">
              <table class="table table-responsive">
                <h4>Available Course(s)</h4>
                <tr v-for="(course, key) in courses" :key="key" class="mt-2">
                  <td class="mt-2"> {{ course.course_Name }} </td>
                  <td class="mt-2"> <button class="btn btn-primary mt-2 bg-primary text-light2" @click="selectCourse(course)">Select</button> </td>
                </tr>
              </table>
            </div>
            <div class="col-lg-6">
              <table class="table table-responsive">
                <h4>Course(s) Applied</h4>
                <tr v-for="(included_course, key) in included_courses" :key="key">
                  <td class="mt-2"> {{ included_course.course_Name }} </td>
                  <td class="mt-2"><button class="btn btn-danger bg-danger text-light mt-2" @click="removeCourse(included_course)">Remove</button> </td>
                </tr>
              </table>
            </div>
          </div>
          <div class="col-6 offset-6 d-flex justify-content-between">
            <button type="button" class="mt-4 btn btn-success float-right w-100 apply" @click="apply()">Apply</button>
            <button type="button" class="mt-4 btn btn-secondary float-right w-100" data-bs-dismiss="modal" aria-label="Close" @click="closeModal">Cancel</button>
          </div>
        </div>
        <div v-else>
          <p>{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
  import FeedbackTemplateService from "@/api/services/FeedbackTemplateService"

  export default {
  props: {
    feedback_template: Object,
  },
  data() {
    return {
      courses: [],
      included_course: [],
      error: false,
      errorMessage: ''
    }
  },
  methods: {
    closeModal() {
      this.$emit("close-modal");
      this.$emit('model-after-action-close', true);
    },
    async fetchData() {
      try {
        if(this.feedback_template.template_ID) {
          const response = await FeedbackTemplateService.getCourseNamesByFeedbackTemplateId(this.feedback_template.template_ID)
          console.log(response)
          if(response.code == 200) {
            this.courses = response.course_name_no_template;
            this.included_courses = response.course_names_using;
            console.log(this.courses)
            console.log(this.included_courses)
          } else {
            this.error = true;
            this.errorMessage = response.message
          }
        }
      } catch (error) {
        this.error = true;
        this.errorMessage = 'Error fetching template by ID:' + error
      }
    },
    selectCourse(course) {
      const index = this.courses.findIndex((c) => c.course_ID === course.course_ID && c.course_Name === course.course_Name);
      if (index !== -1) {
        this.courses.splice(index, 1);
      }
      this.included_courses.push(course)
    },
    removeCourse(course) {
      const index = this.included_courses.findIndex((c) => c.course_ID === course.course_ID && c.course_Name === course.course_Name);
      if (index !== -1) {
        this.included_courses.splice(index, 1);
      }
      this.courses.push(course)
    },
    apply(){
      console.log(this.courses);
      console.log(this.included_courses);
      console.log(this.feedback_template.template_ID);
    }
  },
  mounted() {
    this.fetchData();
  }
  };
  </script>

  <style scoped>
  table td {
    border-style: none;
  }

  .btn.apply {
    margin-right: 20px;
  }
  </style>