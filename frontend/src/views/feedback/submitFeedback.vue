<template>
    <div>
      <div class="container" v-if="!haveError">
        <div class="text-center pb-5 pt-5">
          <h2>{{ headingTitle }}</h2>
          <h4 class="text-grey">{{ this.course.run_Name }}</h4>
        </div>

        <div class="form-group row" v-for="(element, key) in templateData" :key="key">
          <text-field :disabled="disabled" :placeholder="element.answer"  v-if="element.selectedInputType=='Text Field'" class="mb-5" :label="element.question" :qnNum="key+1" @input="updateAnswer"></text-field>
          <number-field :disabled="disabled" :placeholder="element.answer" v-else-if="element.selectedInputType=='Number Field'"  class="mb-5" :label="element.question" :qnNum="key+1" @input="updateAnswer"></number-field>
          <radio-button-field :disabled="disabled" :sOption="element.answer" v-else-if="element.selectedInputType=='Radio Button'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1" @input="updateAnswer"></radio-button-field>
          <single-select-field :disabled="disabled" :sOption="element.answer" v-else-if="element.selectedInputType=='Single Select'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1"  @input="updateAnswer"></single-select-field>
          <likert-scale-field :disabled="disabled" :sOption="element.answer" v-else-if="element.selectedInputType=='Likert Scale'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1" @input="updateAnswer"></likert-scale-field>
        </div>

        <div class="form-group row" v-for="(element, key) in common_questions" :key="key">
          <text-area-field :disabled="disabled" :placeholder="element.answer" v-if="element.selectedInputType=='Text Field'"  class="mb-5" :label="element.question" :qnNum="templateData.length+key+1" @input="updateAnswer"></text-area-field>
          <likert-scale-field :disabled="disabled" :sOption="element.answer" v-else-if="element.selectedInputType=='Likert Scale'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="templateData.length+key+1" @input="updateCommonLikert"></likert-scale-field> 
        </div>
  
        <div class="row">
          <div class="col-12 form-group">
            <button type="button" :disabled="disabled" :title="disabled ? 'Unable to submit, please ensure that all fields have been filled.' : ''" class="btn btn-edit shadow-sm w-100 mt-5" @click="submit">
              Submit
            </button>
          </div>
        </div>
      </div>
      <div class="container" v-else>
        <div class="text-center pb-5">
          <h2>{{ headingTitle }}</h2>
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
import TextAreaField from "@/components/feedbackTemplate/TextAreaField.vue";
import DefaultModal from "@/components/DefaultModal.vue";
import UserService from "@/api/services/UserService.js";
import CourseService from "@/api/services/CourseService.js";
import FeedbackService from "@/api/services/FeedbackService.js";
  
export default {
  components: {
    TextField,
    NumberField,
    RadioButtonField,
    SingleSelectField,
    LikertScaleField,
    TextAreaField,
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
      disabled: false,
      common_questions: [],
      headingTitle: ""
    }
  },
  methods: {
    isWithinFeedbackPeriod(start_date, start_time, end_date, end_time) {
      const feedbackStartDate = new Date(`${start_date} ${start_time}`);
      const feedbackEndDate = new Date(`${end_date} ${end_time}`);
      const currentDateTime = new Date();
      return currentDateTime >= feedbackStartDate && currentDateTime <= feedbackEndDate;
    },
    async loadData() {
      try {
        const course_id = this.$route.params.id;
        this.course = await RunCourseService.getRunCourseById(course_id);
        const withinFeedbackPeriod = this.isWithinFeedbackPeriod(this.course.feedback_Startdate, this.course.feedback_Starttime, this.course.feedback_Enddate, this.course.feedback_Endtime)
        if (!withinFeedbackPeriod) {
          this.disabled = true;
          this.showAlert = true;
          this.haveError = true
          this.title = "Submit Feedback Fail";
          this.message = "Feedback not yet open for submission";
          this.buttonType = "danger"
        } else {
          console.log(this.course)
          this.haveError = false
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
            this.errorMsge = response.message
          }
          const common_response = await FeedbackTemplateService.getFeedbackTemplateCommonQuestions()
          console.log(common_response)
          if (common_response.code == 200){
            this.common_questions = common_response.common_questions
            for (let i = 0; i < this.common_questions.length; i++) {
              this.common_questions[i]['answer'] = '';
            }
          } else {
            this.disabled = true;
            this.haveError = true
            this.errorMsge = common_response.common_questions;
          }
        }
      } catch (error) {
        console.log(error) 
        this.disabled = true;
        this.haveError = true
        this.errorMsge = "Submit Feedback error"
      }
    },
    async getStudentFeedback() {
      try {
        this.disabled = true;
        const course_id = this.$route.params.id;
        this.course = await RunCourseService.getRunCourseById(course_id);
        this.haveError = false
        const response = await FeedbackService.getStudentFeedbackIncludingAnswersAndTemplate(course_id)
        console.log(response)
        if (response.code == 200) {
          this.haveError = false
          this.templateData = response.question_response.data
          console.log(this.templateData)
          this.common_questions = response.common_question_response
        } else {
          this.haveError = true
          this.errorMsge = response.message
        }
      } catch (error) {
        console.log(error) 
        this.disabled = true;
        this.haveError = true
        this.errorMsge = "Submit Feedback error"
      }
    },
    async checkCourseCompleted() {
      try {
      const course_id = this.$route.params.id;
      let course_completed_response = await CourseService.isCourseCompleted(course_id);
      console.log(course_completed_response)
      if (course_completed_response.code == 200) {
        if (course_completed_response.isCourseCompleted == true && course_completed_response.isFeedbackDone == false) {
          this.haveError = false;
          this.headingTitle = "Submit Feedback for";
          this.loadData();
        } else if (course_completed_response.isCourseCompleted == true && course_completed_response.isFeedbackDone == true) {
          this.haveError = false
          this.headingTitle = "View Feedback for";
          this.getStudentFeedback(); 
        } else {
          this.$router.push({ name: 'studentViewProfile' }); 
        }
      } else {
        this.disabled = true;
        this.haveError = true
        this.errorMsge = course_completed_response.message;
      }
      } catch(error) {
        console.log(error)
        this.disabled = true;
        this.haveError = true
        this.errorMsge = "Submit Feedback error"
      }
    },
    async submit()  {
      const rcourse_id = this.course.rcourse_ID;
      const template_id = this.course.template_ID
      const data = {
        'rcourse_id': rcourse_id,
        'template_id': template_id,
        'user_id': this.user_ID,
        'data': this.templateData,
        'common_questions_data': this.common_questions
      }
      console.log(data)
      console.log(this.common_questions)
      const isAnyAnswerBlank = this.templateData.some((element) => {
        return !element.answer.toString().trim();
      });
      const isCommonAnswerBlank = this.common_questions.some((element) => {
        return !element.answer.toString().trim();
      });
      if (!isAnyAnswerBlank && !isCommonAnswerBlank) {
        try{
          const response = await FeedbackService.postStudentFeedback(data)
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
        this.templateData[index]['answer'] = answer.value;
      } else {
        if (answer.value != undefined) {
          this.common_questions[1]['answer'] = answer.value;
        }
      }
    },
    updateCommonLikert(answer) {
      this.common_questions[0]['answer'] = answer.value;
      console.log(this.common_questions);
    }
  },
  async created() {
    const user_ID = await UserService.getUserID();
    this.user_ID = user_ID
    const role = await UserService.getUserRole(user_ID);
    if (role == 'Admin') {
      this.$router.push({ name: 'adminViewCourse' }); 
    } else if (role == 'Instructor' || role == 'Trainer') {
      this.$router.push({ name: 'instructorTrainerViewVotingCampaign' }); 
    } else {
      this.checkCourseCompleted();
    }
  },
}

</script>
  
 