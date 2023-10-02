<template>
    <div>
      <div class="container" v-if="!haveError">
        <div class="text-center pb-5">
          <h2>Submit Feedback</h2>
          <h4 class="text-grey">{{ this.course.course_Name }}</h4>
        </div>

        <div class="form-group row mb-4" v-for="(element, key) in templateData" :key="key">
          <text-field :disabled="disabled" v-if="element.selectedInputType=='Text Field'"  class="mb-4" :label="element.question" :qnNum="key+1" @input="updateAnswer"></text-field>
          <number-field :disabled="disabled" v-else-if="element.selectedInputType=='Number Field'"  class="mb-4" :label="element.question" :qnNum="key+1" @input="updateAnswer"></number-field>
          <radio-button-field :disabled="disabled" v-else-if="element.selectedInputType=='Radio Button'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1" @input="updateAnswer"></radio-button-field>
          <single-select-field :disabled="disabled" v-else-if="element.selectedInputType=='Single Select'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1"  @input="updateAnswer"></single-select-field>
          <likert-scale-field :disabled="disabled" v-else-if="element.selectedInputType=='Likert Scale'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1" @input="updateAnswer"></likert-scale-field> 
        </div>
  
        <div class="row">
          <div class="col-12 form-group">
            <button type="button" class="btn btn-edit shadow-sm w-100 mt-5" @click="submit">
              Submit
            </button>
          </div>
        </div>
      </div>
      <div class="container" v-else>
        <div class="text-center pb-5">
          <h2>Submit Feedback</h2>
        </div>
        <p>{{ errorMsge }}</p>
      </div>

      <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />

    </div>
  </template>
    
<script>
import FeedbackTemplateService from "@/api/services/FeedbackTemplateService.js";
import RunCourseService from "@/api/services/runCourseService.js";
import TextField from "@/components/feedbackTemplate/TextField.vue";
import NumberField from "@/components/feedbackTemplate/NumberField.vue";
import RadioButtonField from "@/components/feedbackTemplate/RadioButtonField.vue";
import SingleSelectField from "@/components/feedbackTemplate/SingleSelectField.vue";
import LikertScaleField from "@/components/feedbackTemplate/LikertScaleFIeld.vue";
import DefaultModal from "@/components/DefaultModal.vue";
  
export default {
  components: {
    TextField,
    NumberField,
    RadioButtonField,
    SingleSelectField,
    LikertScaleField,
    DefaultModal
  },
  data(){
    return {
      course: {},
      templateData: [],
      haveError: false,
      errorMsge: '',
      title: "",
      message: "",
      buttonType: "",
      showAlert: false,
      submitError: false,
      disabled: false
    }
  },
  methods: {
    async loadData() {
      try {
        const course_id = this.$route.params.id;
        const course_response = await RunCourseService.getRunCourseById(course_id)
        console.log(course_response)
        if(course_response.code == 200) {
          this.haveError = false
          this.course = course_response.course
          const response = await FeedbackTemplateService.getTemplateById(this.course.template_ID)
          console.log(response)
          if (response.code == 200) {
            this.haveError = false
            this.templateData = response.data.template.data
            for (let i = 0; i < this.templateData.length; i++) {
              this.templateData[i]['answer'] = '';
            }
          } else {
            this.disabled = true;
            this.haveError = true
            this.errorMsge = course_response.message
            alert(this.errorMsge)
          }
        } else {
          this.disabled = true;
          this.haveError = true
          this.errorMsge = course_response.message
        }
      } catch (error) { 
        this.disabled = true;
        this.haveError = true
        this.errorMsge = error.response.data.message.toString();
      }
    },
    async submit()  {
      const rcourse_id = this.course.rcourse_ID;
      const template_id = this.course.template_ID
      const user_id = 1
      const data = {
        'rcourse_id': rcourse_id,
        'template_id': template_id,
        'user_id': user_id,
        'data': this.templateData
      }
      const isAnyAnswerBlank = this.templateData.some((element) => {

        return !element.answer.trim();
      });
      if (!isAnyAnswerBlank) {
        try{
          const response = await FeedbackTemplateService.postStudentFeedback(data)
          console.log(response)
          if (response.code == 200) {
            this.submitError = false
            this.showAlert = true;
            this.title = "Submit Feedback Success";
            this.message = response.message;
            this.buttonType = "success";
          } else {
            this.submitError = true
            this.showAlert = true;
            this.title = "Submit Feedback Fail";
            this.message = response.message;
            this.buttonType = "danger"
          }
          } catch (error) {
            this.submitError = true
            this.showAlert = true;
            this.title = "Submit Feedback Fail";
            this.message = error.response.data.message.toString();
            this.buttonType = "danger"
        }
      } else {
        this.submitError = true
        this.showAlert = true;
        this.title = "Submit Feedback Fail";
        this.message = "Please answer every question before submitting your feedback."
        this.buttonType = "danger"
      }
    },
    handleModalClosed(value) {
        this.showAlert = value;
        if(!this.showAlert && !this.submitError) {
            this.$router.push('/studentViewProfile');
        }
    },
    updateAnswer(answer) {
      var index = parseInt(answer.key)
      if (this.templateData[index]) {
        this.templateData[index]['answer'] = answer.value
      }
    },
  },
  async created() {
    this.loadData();
  },
}

</script>
  
 