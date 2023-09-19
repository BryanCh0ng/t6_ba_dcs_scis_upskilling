<template>
  <div>
    <div class="container">
      <div class="text-center">
        <h2>Feedback Template</h2>
        <h4 class="text-grey">Customized feedback for a specific course</h4>
      </div>
      <h4 class="mt-5 mb-3">Edit Feedback Template</h4>
      <div class="form-group row mb-4">
        <label class="mb-1">Enter Feedback Template Name</label>
        <input type="text" v-model="feedback_template_name" class="form-control" placeholder="Feedback Template Name">
        <div v-if="v$.feedback_template_name.$error && v$.feedback_template_name.$dirty" class="error-message mt-1 text-danger">Feedback Template Name Field is required.</div>
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
            class="btn btn-secondary mt-5 mb-5 col-12"
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
          <button type="button" class="btn btn-primary shadow-sm w-100 mt-5" @click="openModal" data-bs-toggle="modal" data-bs-target="#preview_modal">
            Preview
          </button>
        </div>

        <div class="col-6 form-group">
          <button type="submit" @click="submitFeedbackTemplate" class="btn btn-edit shadow-sm w-100 mt-5">
            Save Changes
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
  data() {
    return {
      questions: {
        "feedback_template_name": "name",
        "data": [
          {
            "question": "qn1",
            "selectedInputType": "Text Field",
          },
          {
            "question": "qn2",
            "selectedInputType": "Number Field",

          },
          {
            "question": "qn3",
            "selectedInputType": "Likert Scale",
            "inputOptions": [
              {
                "option": "option"
              }
            ],
          },
          {
            "question": "a4",
            "selectedInputType": "Radio Button",
            "inputOptions": [
              {
                "option": "4",
              }
            ],
          },
          {
            "question": "f",
            "selectedInputType": "Single Select",
            "inputOptions": [
              {
                "option": "a",
              }
            ],
          }
        ]
      },
      templateData: {},
      question: ''
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
    submitFeedbackTemplate() {
      var haveError = false
      if (this.v$.feedback_template_name.$error && this.v$.feedback_template_name.$dirty) {
        haveError = true;
      }
      var formData = this.getFormData();
      console.log(formData)
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
      var haveError = false;

      let formDataArray = [];
      if (Array.isArray(feedbackTemplates)) {
        feedbackTemplates.forEach((feedbackTemplate) => {
          if (feedbackTemplate) {
            const formData = feedbackTemplate.submitData();
            if (formData.haveError) {
              haveError = true;
            }
            formDataArray.push(formData);
          }
        });
      } else if (feedbackTemplates) {
        const formData = feedbackTemplates.submitData();
        if (formData.haveError) {
          haveError = true;
        }
        formDataArray.push(formData);
      }
      console.log(haveError)
      console.log(formDataArray)
      return formDataArray;
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
    }
  },
  created() {
    this.questions.data.forEach((data, index) => {
      data.id = index + 1;
      data.originalQnNum = index + 1;
      data.qnNum = index + 1;
      data.edit = true
      data.haveError = false
    });
    this.feedback_template_name = this.questions.feedback_template_name;
    console.log(this.questions)
    console.log(this.questions.data)
  }
};
</script>

<style scoped>
.addQn {
  cursor: pointer;
}
</style>
