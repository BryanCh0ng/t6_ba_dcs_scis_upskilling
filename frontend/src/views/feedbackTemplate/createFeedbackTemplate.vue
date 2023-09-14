<template>
  <div>
    <div class="container">
      <div class="form-group mt-2 mb-2" v-for="(element, index) in questions" :key="element.id">
        <feedback-template :originalQnNum="element.originalQnNum" v-if="!element.destroyed" :destroyed="element.destroyed" 
        :id="element.id" @destroy-me="destroyChild" :qnNum="element.qnNum" @templateDataChanged="handleTemplateDataChange" 
        @removeQuestion="removeQuestion(index)"></feedback-template>
        <div>
          <button  v-if="!element.destroyed" @click="destroyComponent(element.id)" class="btn btn-secondary mt-5 mb-5 col-12">
            Remove Question {{ element.qnNum }}
          </button>
        </div>
      </div>
      <div>
        <a class="mt-5 d-flex justify-content-center text-dark addQn" @click="addQuestion">+ Add Question</a>
      </div>
      <button class="btn btn-edit w-100 mt-5" @click="submitFeedbackTemplate">Submit</button>
    </div>
  </div>
</template>
  
<script>
import FeedbackTemplate from "@/components/field/FeedbackTemplateField.vue";

export default {
  components: {
    FeedbackTemplate
  },
  data(){
    return {
      qnNum: 1,
      templateData: {},
      questions: []
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
      console.log(this.templateData);
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
    }
  }
}

</script>

<style scoped>
  .addQn {
    cursor: pointer;
  }
</style>
