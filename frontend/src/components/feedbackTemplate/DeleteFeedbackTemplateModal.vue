<template>
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body pt-1"> 
        <div class="modal-title pt-3">
          <h3 class="text-center">Delete {{ feedback_template.template_Name }}</h3>
        </div>
        <div v-if="!error">
          <p class="text-success">{{ deleteMsge }}</p>
          <div class="mt-3">
              This Action cannot be undone.  Once {{ feedback_template.template_Name }} is deleted, the following courses will no longer be able to receive feedback: 
          </div>
          <div class="mt-3">
            <h6 class="font-weight-bold">Course(s):</h6>
            <ul>
              <li v-for="(course, key) in courses" :key="key">{{ course.course_Name }}
                <ul>
                  <li v-for="(run, runKey) in course.run" :key="runKey">
                    {{ run.run_Name }}</li>
                </ul>
              </li>
            </ul>
          </div>
          <div class="col-6 offset-6 d-flex justify-content-between">
            <button type="button" :disabled="disabled" :title="disabled ? 'Unable to delete feedback template due to ongoing/past feedback period' : ''" class="mt-4 btn delete btn-danger float-right w-100"  @click="deleteTemplate">Delete</button>
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
    deleteModalOpen: Boolean
  },
  data() {
    return {
      courses: {},
      error: false,
      errorMessage: '',
      deleteMsge: '',
      disabled: false,
      expandedCourses: []
    }
  },
  methods: {
    closeModal() {
      const button = document.getElementById("delete-feedback-template");
      button.disabled = false;
      this.$emit("close-modal");
      this.$emit('model-after-action-close', true);
    },
    async fetchData() {
      this.deleteMsge = ''
      this.error = false
      this.errorMessage = ''
      this.disabled = false
      this.courses = {}
      try {
        const response = await FeedbackTemplateService.getCoursesByTemplateId(this.feedback_template.template_ID)
        console.log(response)
        if(response.code == 200) {
          this.courses = response.data.courses
        } else {
          this.error = true;
          this.errorMessage = response.message
        }
      } catch (error) {
        this.error = true;
        this.errorMessage = 'Error fetching template by ID:' + error
      }
    },
    async deleteTemplate() {
      try {
        const response = await FeedbackTemplateService.deleteFeedbackTemplate(this.feedback_template.template_ID)
        console.log(response)
        if (response.code == 200) {
          this.error = false
          this.deleteMsge = response.message
          this.disabled = true
        } else {
          this.error = true
          this.errorMessage = response.message
        }
      } catch (error) {
        console.log(error)
        this.error = true;
        // this.errorMessage = error.toString()
      }
    }
  },
  watch: {
    deleteModalOpen() {
      this.fetchData(); 
    },
  },
  mounted() {
    this.fetchData(); 
  },
  };
  </script>

  <style scoped>
  .btn.delete {
    margin-right: 20px;
  }

  </style>

