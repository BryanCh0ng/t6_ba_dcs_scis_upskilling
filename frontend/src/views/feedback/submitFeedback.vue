<template>
    <div>
      <div class="container" v-if="!haveError">
        <div class="text-center pb-5">
          <h2>Submit Feedback</h2>
          <h4 class="text-grey">{{ this.course.course_Name }}</h4>
        </div>

        <div class="form-group row mb-4" v-for="(element, key) in templateData" :key="key">
          <text-field v-if="element.selectedInputType=='Text Field'"  class="mb-4" :label="element.question" :qnNum="key+1" @input="updateAnswer"></text-field>
          <number-field v-else-if="element.selectedInputType=='Number Field'"  class="mb-4" :label="element.question" :qnNum="key+1" @input="updateAnswer"></number-field>
          <radio-button-field v-else-if="element.selectedInputType=='Radio Button'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1" @input="updateAnswer"></radio-button-field>
          <single-select-field v-else-if="element.selectedInputType=='Single Select'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1"  @input="updateAnswer"></single-select-field>
          <likert-scale-field v-else-if="element.selectedInputType=='Likert Scale'" class="mb-4" :options="element.inputOptions" :label="element.question" :qnNum="key+1" @input="updateAnswer"></likert-scale-field> 
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
    </div>
  </template>
    
<script>
import FeedbackTemplateService from "@/api/services/FeedbackTemplateService.js";
import CourseService from "@/api/services/CourseService.js";
import TextField from "@/components/feedbackTemplate/TextField.vue";
import NumberField from "@/components/feedbackTemplate/NumberField.vue";
import RadioButtonField from "@/components/feedbackTemplate/RadioButtonField.vue";
import SingleSelectField from "@/components/feedbackTemplate/SingleSelectField.vue";
import LikertScaleField from "@/components/feedbackTemplate/LikertScaleFIeld.vue";

  
export default {
  components: {
    TextField,
    NumberField,
    RadioButtonField,
    SingleSelectField,
    LikertScaleField
  },
  data(){
    return {
      course: {},
      templateData: [],
      haveError: false,
      errorMsge: '',
    }
  },
  methods: {
    async loadData() {
      this.answers = new Array(this.templateData.length).fill('');
      const course_id = this.$route.params.id;
      const course_response = await CourseService.getCourseById(course_id)
      if(course_response.code == 200) {
        this.haveError = false
        this.course = course_response.data.course[0]
        const response = await FeedbackTemplateService.getTemplateById(this.course.template_ID)
        if (response.code == 200) {
          this.haveError = false
          this.templateData = response.data.template.data
          console.log(this.templateData)
        } else {
          this.haveError = true
          this.errorMsge = course_response.message
          alert(this.errorMsge)
        }
      } else {
        this.haveError = true
        this.errorMsge = course_response.message
      }
    },
    submit() {
      const course_id = this.course.course_ID;
      const template_id = this.course.template_ID
      const user_id = 1
      const data = {
        'course_id': course_id,
        'template_id': template_id,
        'user_id': user_id,
        'data': this.templateData
      }
      console.log(data)
    },
    updateAnswer(answer) {
      var index = parseInt(answer.key)
      if (this.templateData[index]) {
        this.templateData[index]['answer'] = answer.value
      }
    },
  },
  created() {
    this.loadData();
  },
}

</script>
  
 