<template>
  <div>
    <div class="container pt-4">
      <div class="text-center">
        <h2>Feedback Template</h2>
        <h4 class="text-grey">Customized feedback for a specific course</h4>
      </div>
      <h4 class="mt-5 mb-3">Edit Feedback Template</h4>

      <div class="form-group row mb-4 pt-4 pb-4 bg-light-grey">
        <div>
          <h5>Common Required Questions (will be placed at the end of feedback)</h5>
        </div>
        <div class="form-group">
          <label>1. Question To Ask</label>
          <textarea disabled="true" class="form-control" type="text" :placeholder="'How would you rate the course?'"></textarea>
        </div>
        <div class="form-group mt-2">
          <label>1. Input Type</label>
          <input disabled="true" class="form-control" type="text" :placeholder="'Likert Scale'" />
        </div>
        <div class="form-group mt-2">
          <label>1. Likert Scale Option (Sequence from left to right)</label>
          <ul>
            <li>
              <input type="radio" disabled>
              <label>Very Poor</label>
            </li>
            <li>
              <input type="radio" disabled>
              <label>Poor</label>
            </li>
            <li>
              <input type="radio" disabled>
              <label>Neutral</label>
            </li>
            <li>
              <input type="radio" disabled>
              <label>Good</label>
            </li>
            <li>
              <input type="radio" disabled>
              <label>Excellent</label>
            </li>
          </ul>
        </div>
        <div class="form-group">
          <label>2. Question To Ask</label>
          <input disabled="true" class="form-control" type="text" :placeholder="'Any Feedbacks for the course?'" />
        </div>
        <div class="form-group mt-2">
          <label>2. Input Type</label>
          <input disabled="true" class="form-control" type="text" :placeholder="'Text Field'" />
        </div>
      </div>

      <div v-if="!questionsError">
        <div class="form-group row mb-4">
          <label class="mb-1">Enter Feedback Template Name</label>
          <input type="text" v-model="feedback_template_name" class="form-control" placeholder="Feedback Template Name">
          <div v-if="v$.feedback_template_name.$error && v$.feedback_template_name.$dirty" class="error-message mt-1 text-danger">Feedback Template Name Field is required.</div>
          <div v-if="this.isPresent" class="error-message mt-1 text-danger">{{ templateNameErrorMsge }}</div>
        </div>

        <div class="form-group mt-2 mb-2" v-for="(element, index) in questions.data" :key="element.id">
          <feedback-template
            ref="feedbackTemplates"
            :originalQnNum="element.originalQnNum"
            v-if="!element.destroyed"
            :destroyed="element.destroyed"
            :id="element.id"
            :existingFeedbackTemplate = "element"
            @destroy-me="destroyChild"
            :qnNum="element.qnNum"
            @templateDataChanged="handleTemplateDataChange"
            @removeQuestion="removeQuestion(index)"
          ></feedback-template>
          <div>
            <button
              v-if="!element.destroyed"
              @click="destroyComponent(element.id)"
              class="btn btn-secondary mt-5 mb-5 col-12" title="Remove Question"
            >
              Remove Question {{ element.qnNum }}
            </button>
          </div>
        </div>

        <div>
          <a class="mt-4 d-flex justify-content-center text-dark addQn" @click="addQuestion">+ Add Question</a>
        </div>
        <div class="row">
          <div class="col-6 form-group">
            <button type="button" class="btn btn-primary shadow-sm w-100 mt-5" @click="openModal" data-bs-toggle="modal" data-bs-target="#preview_modal" title="Preview">
              Preview
            </button>
          </div>

          <div class="col-6 form-group">
            <button type="submit" @click="submitFeedbackTemplate" class="btn btn-edit shadow-sm w-100 mt-5" title="Save Changes">
              Save Changes
            </button>
          </div>
        </div>
      </div>
      <div v-else-if="questionsError">
        <p>{{ questionsErrorMessage }}</p>
      </div>
    </div>
    <div class="modal fade" id="preview_modal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <preview-modal :feedbackTemplate="templateData" @close-modal="closeModal" />
      </div>
    </div>

    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />

  </div>
</template>

<script>
import FeedbackTemplate from "@/components/feedbackTemplate/FeedbackTemplateField.vue";
import PreviewModal from "@/components/feedbackTemplate/PreviewModal.vue";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { ref } from "vue";
import FeedbackTemplateService from "@/api/services/FeedbackTemplateService.js";
import DefaultModal from "@/components/DefaultModal.vue";
import UserService from "@/api/services/UserService.js";

export default {
  components: {
    FeedbackTemplate,
    PreviewModal,
    DefaultModal
  },
  setup() {
    const feedback_template_name = ref('');

    const rules = {
      feedback_template_name: { required }
    };

    const v$ = ref(useVuelidate(rules, {feedback_template_name}));
    v$.value.$touch();

    return {
      v$, 
      feedback_template_name
    };
  },
  data() {
    return {
      questions: {},
      templateData: {},
      question: '',
      questionsError: false,
      questionsErrorMessage: '',
      isPresent: false,
      templateNameErrorMsge: '',
      showAlert: false,
      message: '',
      buttonType: '',
      title: ''
    };
  },
  methods: {
    addQuestion() {
      const newId = this.questions.data.length + 1;
      this.questions.data.push({
        id: newId,
        destroyed: false,
        originalQnNum: newId
      });
      this.updateQuestionNumbers();
    },
    destroyComponent(id) {
      console.log(this.questions.data)
      const component = this.questions.data.find(c => c.id === id);
      if (component) {
        component.destroyed = true;
        this.updateQuestionNumbers();
      }
    },
    async submitFeedbackTemplate() {
      var haveError = false
      if (this.v$.feedback_template_name.$error && this.v$.feedback_template_name.$dirty) {
        haveError = true;
      }
      var formData = this.getFormData();
      console.log(formData)
      if (formData.some(item => item.haveError === true)) {
        haveError = true
      }

      const get_all_template_name_response = await FeedbackTemplateService.getAllFeedbackTemplateNames()
      if(get_all_template_name_response.code == 200) {
        var index = get_all_template_name_response.feedback_template_names.indexOf(this.feedback_template_name)
        if (index !== -1) {
          get_all_template_name_response.feedback_template_names.splice(index, 1); 
        }
        console.log(get_all_template_name_response.feedback_template_names)
        var convert_to_lower_case = get_all_template_name_response.feedback_template_names.map(function(item) {
              return item.toLowerCase();
          });
        this.isPresent = convert_to_lower_case.includes(this.feedback_template_name.toLowerCase());
        if(this.isPresent) {
          haveError = true
        }
        this.templateNameErrorMsge = "Feedback Template Name already exists."
      } else {
        haveError = true
        this.templateNameErrorMsge = get_all_template_name_response.message
      }

      if (!haveError && !this.questionsError) {
        const data = {
          feedback_template_name: this.feedback_template_name,
          template_id: this.$route.params.id,
          data: formData
        }
        try {
          console.log(data)
          const response = await FeedbackTemplateService.editFeedbackTemplate(this.$route.params.id,data)
          if (response.code == 200) {
            this.title = "Feedback Template Edit Success"
            this.message =  response.message
            this.buttonType = "success"
            this.showAlert = !this.showAlert;
          } else {
            this.title = "Feedback Template Edit Failed"
            this.message = response.message
            this.buttonType = "danger"
            this.showAlert = !this.showAlert;
          }
        } catch (error) {
            this.title = "Feedback Template Edit Failed";
            this.message = error.response.data.message.toString();
            this.buttonType = "danger"
            this.showAlert = !this.showAlert;
            // throw new Error("Feedback Template Edit was unsuccessful");
        }
      }
    },
    getFormData() {
      const feedbackTemplates = this.$refs.feedbackTemplates;
      let formDataArray = [];
      if (Array.isArray(feedbackTemplates)) {
        feedbackTemplates.forEach((feedbackTemplate) => {
          if (feedbackTemplate) {
            const formData = feedbackTemplate.submitData();
            formDataArray.push(formData);
          }
        });
      } else if (feedbackTemplates) {
        const formData = feedbackTemplates.submitData();
        formDataArray.push(formData);
      }
      return formDataArray
    },
    handleTemplateDataChange(data) {
      console.log(data)
      this.templateData[data.originalQnNum - 1] = data;
    },
    updateQuestionNumbers() {
      let qnNum = 1;
      this.questions.data.forEach((question) => {
        if (!question.destroyed) {
          question.qnNum = qnNum;
          qnNum++;
        }
      });
      console.log(this.questions)
    },
    openModal() {
      this.templateData = this.getFormData();
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    async handleModalClosed(value){
      this.showAlert = value;
      if (!this.showAlert) {
        this.$router.push('/adminViewFeedbackTemplate');
      }
    }
  },
  async created() {
    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);
    if (role == 'Student') {
      this.$router.push({ name: 'studentViewCourse' }); 
    } else if (role == 'Instructor' || role == 'Trainer') {
      this.$router.push({ name: 'instructorTrainerViewVotingCampaign' });
    } else {
      const template_id = this.$route.params.id;
      try {
        if(template_id) {
          const response = await FeedbackTemplateService.getTemplateById(template_id);
          if (response.code == 200) {
            this.questions = response.data.template
            this.questionsError = false
            this.questions.data.forEach((data, index) => {
              data.id = index + 1;
              data.originalQnNum = index + 1;
              data.qnNum = index + 1;
              data.edit = true
              data.haveError = false
            });
            this.feedback_template_name = this.questions.feedback_template_name;
          } else {
            this.questionsError = true
            this.questionsErrorMessage = "Error fetching template by ID"
          }
        }
        else {
          this.questionsError = true
          this.questionsErrorMessage = "feedback template non existent"
        }
      } catch (error) {
        this.questionsError = true
        this.questionsErrorMessage = 'Error fetching template by ID:' + error
        console.error('Error fetching template by ID:', error);
      }
    }
  }
};
</script>

<style scoped>
.addQn {
  cursor: pointer;
}
</style>
