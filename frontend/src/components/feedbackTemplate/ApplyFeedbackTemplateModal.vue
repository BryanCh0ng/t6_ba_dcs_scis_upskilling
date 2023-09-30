<template>
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body pt-1"> 
        <div class="modal-title pt-3">
          <h3 class="text-center">Apply {{ feedback_template.template_Name }} To Course Run(s)</h3>
        </div>
        <div v-if="!error">
          <div class="row mt-5">
            <div class="col-lg-6">
              <table class="table table-responsive">
                <h4>Available Course Run(s)</h4>
                <tr v-for="(course, key) in not_included_courses" :key="key" class="mt-2">
                  <td class="mt-2"> {{ course.run_Name }} </td>
                  <td class="mt-2"> <button class="btn btn-primary mt-2 bg-primary text-light" @click="selectCourse(course)">Select</button> </td>
                </tr>
              </table>
            </div>
            <div class="col-lg-6">
              <table class="table table-responsive">
                <h4>Course Run(s) Applied</h4>
                <tr v-for="(included_course, key) in included_courses" :key="key">
                  <td class="mt-2"> {{ included_course.run_Name }} </td>
                  <td class="mt-2"><button class="btn btn-danger bg-danger text-light mt-2" @click="removeCourse(included_course)">Remove</button> </td>
                </tr>
              </table>
            </div>
          </div>
          <div class="col-6 offset-6 d-flex justify-content-between">
            <button type="button" class="mt-4 btn btn-success float-right w-100 apply" @click="apply()">Apply</button>
            <button type="button" class="mt-4 btn btn-secondary float-right w-100" data-bs-dismiss="modal" aria-label="Close" @click="closeModal">Cancel</button>
          </div>
          <div>
            <p class="text-success text-center pt-5">{{ successMsge }}</p>
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
    modalOpen: Boolean
  },
  data() {
    return {
      not_included_courses: [],
      included_courses: [],
      error: false,
      errorMessage: '',
      successMsge: ''
    }
  },
  methods: {
    closeModal() {
      this.$emit("close-modal");
      this.$emit('model-after-action-close', true);
    },
    async fetchData() {
      try {
        this.not_included_courses = [];
        this.included_courses = [];
        this.error = false;
        this.errorMessage  = '';
        this.successMsge = '';
        if(this.feedback_template.template_ID) {
          const response = await FeedbackTemplateService.getCourseNamesByFeedbackTemplateId(this.feedback_template.template_ID)
          console.log(response)
          if(response.code == 200) {
            this.not_included_courses = response.course_name_no_template;
            this.included_courses = response.course_names_using;
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
      const index = this.not_included_courses.findIndex((c) => c.rcourse_id === course.rcourse_id && c.run_Name === course.run_Name);
      if (index !== -1) {
        this.not_included_courses.splice(index, 1);
      }
      this.included_courses.push(course)
    },
    removeCourse(course) {
      const index = this.included_courses.findIndex((c) => c.rcourse_id === course.rcourse_id && c.run_Name === course.run_Name);
      if (index !== -1) {
        this.included_courses.splice(index, 1);
      }
      this.not_included_courses.push(course)
    },
    async apply(){
      this.error = false; 
      this.errorMessage = '';
      this.successMsge = ''
      const data = {
        not_included_courses: this.not_included_courses,
        included_courses: this.included_courses,
        template_ID: this.feedback_template.template_ID
      }
      console.log(data)
      try {
        const response = await FeedbackTemplateService.applyFeedbackTemplateToCourses(data)
        console.log(response)
        if (response.code == 200) {
          this.error = false
          this.successMsge = response.message
        } else {
          this.error = true
          this.errorMessage = response.message
          this.successMsge = ''
        }
      } catch (error) {
        console.log(error)
        this.error = true;
        this.successMsge = ''
        this.errorMessage = error.toString()
      }
    } 
  },
  watch: {
    modalOpen() {
      this.fetchData(); 
    },
  },
  mounted() {
    this.fetchData(); 
  },
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