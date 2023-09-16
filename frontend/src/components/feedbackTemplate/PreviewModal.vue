<template>
  <div class="modal-content">
    <div class="modal-header">
      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
    </div>
    <div class="modal-body pt-1"> 
      <div class="modal-title pt-3">
        <h5>Feedback Template Preview</h5>
      </div>
      <div class="mt-4" v-for="template in this.feedbackTemplate" :key="template.id">
        <text-field v-if="template.selectedInputType == 'Text Field'" class="mb-4" :label="template.question"></text-field>
        <number-field v-else-if="template.selectedInputType == 'Number Field'" class="mb-4" :label="template.question"></number-field>
        <radio-button-field v-else-if="template.selectedInputType == 'Radio Button'" class="mb-4" :options="template.inputOptions" :label="template.question"></radio-button-field>
        <single-select-field v-else-if="template.selectedInputType == 'Single Select'" class="mb-4" :options="template.inputOptions" :label="template.question"></single-select-field>
        <likert-scale-field v-else-if="template.selectedInputType == 'Likert Scale'"  class="mb-4" :options="template.inputOptions" :label="template.question"></likert-scale-field>
      </div>
    </div>
  </div>
</template>
  
<script>
import TextField from "./TextField.vue";
import NumberField from "./NumberField.vue";
import RadioButtonField from "./RadioButtonField.vue";
import SingleSelectField from "./SingleSelectField.vue";
import LikertScaleField from "./LikertScaleFIeld.vue";

export default {
  props: {
    feedbackTemplate: Object
  },
  components: {
    TextField,
    NumberField,
    RadioButtonField,
    SingleSelectField,
    LikertScaleField
  }
};
</script>