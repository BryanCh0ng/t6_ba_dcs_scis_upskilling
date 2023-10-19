<template>
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeModal"></button>
      </div>
      <div class="modal-body pt-1"> 
        <div class="modal-title pt-3">
          <h3 class="text-center">Apply Feedback Template for {{ course.run_Name }} </h3>
        </div>
        <div v-if="!error">
          <div class="mt-4 mb-4 container form-group row">
            <label class="mb-1">Select Feedback Template for {{ course.run_Name }}</label>
            <select class="form-control" v-model="selectedOption">
              <option disabled selected>Select a Feedback Template</option>
              <option v-for="feedback_template in feedback_templates" :key="feedback_template.template_ID" :value="feedback_template.template_ID">{{ feedback_template.template_Name }}</option>
            </select>
          </div>
          <div>
            <p class="text-success">{{ successMsge }}</p>
          </div>
          <div class="col-6 offset-6 d-flex justify-content-between">
            <button type="button" id="apply-feedback-template-to-course-btn" class="mt-4 btn btn-success float-right w-100 apply" @click="apply()">Apply</button>
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
  import runCourseService from "@/api/services/runCourseService"

  export default {
  props: {
    course: Object,
    modalOpen: Boolean
  },
  data() {
    return {
      error: false,
      errorMessage: '',
      feedback_templates: [],
      selectedOption: '',
      successMsge: ''
    }
  },
  methods: {
    async fetchData() {
      this.error = false;
      this.errorMessage = '';
      this.successMsge = '';
      const button = document.getElementById("apply-feedback-template-to-course-btn");
      button.disabled = false;
      if(this.course.course_ID) {
        this.selectedOption = this.course.template_ID
      } 
      try {
        console.log('created')
        let response = await FeedbackTemplateService.getAllTemplates()
        console.log(response)
        if (response.code == 200) {
          this.error = false;
          this.feedback_templates = response.templates
        } else {
          this.error = true;
          this.errorMessage = response.message
        }
      } catch (error) {
        this.error = true;
        this.errorMessage = error
      }
      console.log(this.selectedOption)
    },
    async apply(){
      try {
        console.log(this.selectedOption)
        console.log(this.course.rcourse_ID)
        const response = await runCourseService.CourseApplyFeedbackTemplate(this.course.rcourse_ID, this.selectedOption)
        console.log(response)
        if (response.code == 200) {
          this.error = false;
          this.successMsge = response.message;
          const button = document.getElementById("apply-feedback-template-to-course-btn");
          button.disabled = true;
        } else {
          this.error = true;
          this.errorMessage = response.message;
        }
      } catch (error) {
        this.error = true;
        this.errorMessage = error
      }
    },
    closeModal() {
      this.$emit("close-modal");
      this.$emit('model-after-action-close', true);
    }
  },
  watch: {
    modalOpen(newVal) {
      console.log(newVal)
      console.log('modal open')
      this.fetchData(); 
    },
  },

  mounted() {
    this.fetchData(); 
  }
  };
  </script>

  <style scoped>
  .btn.apply {
    margin-right: 20px;
  }
  </style>