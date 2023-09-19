<template>
  <div>
    <div class="container">
      <div class="text-center">
        <h2>Feedback Template</h2>
        <h4 class="text-grey">Customised feedbacks for specific course</h4>
      </div>
      <h4 class="mt-5 mb-3">Create Feedback Template</h4>
      <div class="form-group row mb-4">
        <label class="mb-1">Enter Feedback Template Name</label>
        <input type="text" v-model="feedback_template_name" class="form-control" placeholder="Feedback Template Name" required>
        <div v-if="v$.feedback_template_name.$error && v$.feedback_template_name.$dirty" class="error-message mt-1 text-danger">Feedback Template Name Field is required.</div>
      </div>

      <div class="form-group mt-2 mb-2" v-for="(element, index) in questions" :key="element.id">
        <feedback-template ref="feedbackTemplates" 
        :originalQnNum="element.originalQnNum" 
        v-if="!element.destroyed" :destroyed="element.destroyed" 
        :id="element.id" 
        @destroy-me="destroyChild" 
        :qnNum="element.qnNum" 
        @templateDataChanged="handleTemplateDataChange" 
        @removeQuestion="removeQuestion(index)" 
        @submitData="submitData">
        </feedback-template>
        <div>
          <button  v-if="!element.destroyed" @click="destroyComponent(element.id)" class="btn btn-secondary mt-5 mb-5 col-12">
            Remove Question {{ element.qnNum }}
          </button>
        </div>
      </div>
      <div>
        <a class="mt-4 d-flex justify-content-center text-dark addQn" @click="addQuestion">+ Add Question</a>
      </div>
      <div class="row">
        <div class="col-6 form-group">
          <button type="button" class="btn btn-primary shadow-sm w-100 mt-5" @click="openModal" data-bs-toggle="modal" data-bs-target="#preview_modal">
            Preview
          </button>
        </div>

        <div class="col-6 form-group">
          <button type="submit" @click="submitFeedbackTemplate" class="btn btn-edit shadow-sm w-100 mt-5">
            Create
          </button>
        </div>
      </div>
    </div>
    <div class="modal fade" id="preview_modal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <preview-modal :feedbackTemplate="templateData" @close-modal="closeModal" />
      </div>
    </div>
  </div>
</template>
  
<script>
import FeedbackTemplate from "@/components/feedbackTemplate/FeedbackTemplateField.vue";
import PreviewModal from "@/components/feedbackTemplate/PreviewModal.vue";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { ref } from "vue";

export default {
  components: {
    FeedbackTemplate,
    PreviewModal
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
  data(){
    return {
      qnNum: 1,
      templateData: {},
      questions: [],
      question: ''
    }
  },
  methods: {
    addQuestion() {
      const newId = this.qnNum++;
      this.questions.push({
        id: newId,
        destroyed: false,
        originalQnNum: newId
      });
      this.qnNum++;
      this.updateQuestionNumbers();
    },
    destroyComponent(id) {
      const component = this.questions.find(c => c.id === id);
      if (component) {
        component.destroyed = true;
        if (this.templateData[id]) {
          delete this.templateData[id];
        }
        this.updateQuestionNumbers();
      }
    },
    submitFeedbackTemplate() {
      var haveError = false
      if (this.v$.feedback_template_name.$error && this.v$.feedback_template_name.$dirty) {
        haveError = true;
      }
      var formData = this.getFormData();
      if (formData.some(item => item.haveError === true)) {
        haveError = true
      }
      if (haveError == false) {
        const output = {
          feedback_template_name: this.feedback_template_name,
          data: formData
        }
        console.log(output)
        console.log('submitted')
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
      this.templateData[data.originalQnNum] = data;
    },
    updateQuestionNumbers() {
      let qnNum = 1;
      this.questions.forEach((question) => {
        if (!question.destroyed) {
          question.qnNum = qnNum;
          qnNum++;
        }
      });
    },
    openModal() {
      this.getFormData();
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
  }
}

</script>

<style scoped>
  .addQn {
    cursor: pointer;
  }
</style>
