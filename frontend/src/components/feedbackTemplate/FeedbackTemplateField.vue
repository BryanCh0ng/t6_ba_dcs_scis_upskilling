<template>
  <div>
    <div class="form-group mb-4" :class="{ 'form-group--error': v$.question.$error && v$.question.$dirty }">
      <label>{{ qnNum }}. Question To Ask</label>
      <textarea v-model.trim="v$.question.$model" placeholder="Enter Question" class="w-100 mt-2 form-control" required></textarea>
      <div v-if="v$.question.$error && v$.question.$dirty" class="error-message mt-1 text-danger">This field is required.</div>
    </div>
    <div class="form-group mb-4">
      <label>{{ qnNum }}. Input Type</label>
      <dropdown-field v-model="selectedInputType" :default-placeholder="'Text Field'" class="mt-2">
        <option v-for="inputType in inputTypeSelect" :key="inputType" :value="inputType">
          {{ inputType }}
        </option>
      </dropdown-field>
    </div>
    <div v-if="selectedInputType === 'Likert Scale'">
      <label>{{ qnNum }}. Likert Scale (Sequence from left to right)</label>
      <draggable v-model="likertScaleText" tag="v-layout" :group="{ name: 'row' }" class="form-control pb-5 mt-2 mb-2 likert-scale-draggable" item-key="id">
        <template v-slot:item="{ element, index }">
          <div class="mt-3">
            <div class="d-flex mt-2 option-container" :class="index">
              <input class="form-control" v-model="element.option" type="text" :placeholder="'Likert Scale Option'" required />
              <button class="btn btn-danger remove-option" @click="removeOption(element.id)">Remove</button>
            </div>
            <div v-if="likertScaleTextErrors[index]" class="error-message mt-1 text-danger">{{ likertScaleTextErrors[index] }}</div>
          </div>
        </template>
      </draggable>
      <div>
        <a class="d-flex justify-content-center text-dark likert-scale-add" @click="addLikertScaleField">+ Add Likert Scale Option</a>
      </div>
    </div>
    <div v-else-if="selectedInputType === 'Radio Button'">
      <label>{{ qnNum }}. Radio Button (Sequence from top to bottom)</label>
      <draggable v-model="radioButtonText" tag="v-layout" :group="{ name: 'row' }" class="form-control pb-5 mt-2 mb-2 radio-button-draggable" item-key="id">
        <template v-slot:item="{ element, index }">
          <div class="mt-3">
            <div class="d-flex mt-2 option-container" :class="index">
              <input class="form-control" v-model="element.option" type="text" :placeholder="'Radio Button Option'" required />
              <button class="btn btn-danger remove-option" @click="removeOption(element.id)">Remove</button>
            </div>
            <div v-if="radioButtonTextErrors[index]" class="error-message mt-1 text-danger">{{ radioButtonTextErrors[index] }}</div>
          </div>
        </template>
      </draggable>
      <div>
        <a class="d-flex justify-content-center text-dark radio-button-add" @click="addRadioButtonField">+ Add Radio Button Option</a>
      </div>
    </div>
    <div v-else-if="selectedInputType === 'Single Select'">
      <label>{{ qnNum }}. Single Select (Sequence from top to bottom)</label>
      <draggable v-model="singleSelectText" tag="v-layout" :group="{ name: 'row' }" class="form-control pb-5 mt-2 mb-2 single-select-draggable" item-key="id">
        <template v-slot:item="{ element, index }">
          <div class="mt-3">
            <div class="d-flex mt-2 option-container" :class="index">
              <input class="form-control" v-model="element.option" type="text" :placeholder="'Single Select Option'" required />
              <button class="btn btn-danger remove-option" @click="removeOption(element.id)">Remove</button>
            </div>
            <div v-if="singleSelectTextErrors[index]" class="error-message mt-1 text-danger">{{ singleSelectTextErrors[index] }}</div>
          </div>
        </template>
      </draggable>
      <div>
        <a class="d-flex justify-content-center text-dark single-select-add" @click="addSingleSelectField">+ Add Single Select Option</a>
      </div>
    </div>
  </div>
</template>
    
<script>
  import DropdownField from "../../components/forms/DropdownField.vue";
  import draggable from 'vuedraggable';
  import { useVuelidate } from "@vuelidate/core";
  import { required } from "@vuelidate/validators";
  import { ref, computed } from "vue";
  
  export default {
    components: {
      DropdownField,
      draggable
    },
    props: {
      qnNum: Number,
      id: Number,
      destroyed: Boolean,
      originalQnNum: Number
    },
    setup() {
      const question = ref('');
      const likertScaleText = ref([{ id: 1, option: '', displayedId: 1 }]);
      const radioButtonText = ref([{ id: 1, option: '', displayedId: 1 }]);
      const singleSelectText = ref([{ id: 1, option: '', displayedId: 1 }]);
      const selectedInputType = ref('Text Field');

      const rules = {
        question: { required },
        likertScaleText: {},
        radioButtonText: {},
        singleSelectText: {}
      };

      const requiredTextRule = (val) => val.trim() !== '';
  
      const radioButtonTextErrors = computed(() => {
        return radioButtonText.value.map((option) => {
          if (!requiredTextRule(option.option)) {
            return 'This field is required.';
          } else {
            return '';
          }
        });
      });

      const likertScaleTextErrors = computed(() => {
        return likertScaleText.value.map((option) => {
          if (!requiredTextRule(option.option)) {
            return 'This field is required.';
          } else {
            return '';
          }
        });
      });

      const singleSelectTextErrors = computed(() => {
        return singleSelectText.value.map((option) => {
          if (!requiredTextRule(option.option)) {
            return 'This field is required.';
          } else {
            return '';
          }
        });
      });

      const v$  = useVuelidate(rules, {question, likertScaleText, radioButtonText, singleSelectText});

      const isFormValid = true;

      const submitData = () => {
        v$.value.$touch();

        const hasTextareaError = v$.value.$dirty && v$.value.question.$invalid;
        const hasRadioErrors = radioButtonTextErrors.value.some((error) => !!error);
        const hasLikertScaleErrors = likertScaleTextErrors.value.some((error) => !!error);
        const hasSingleSelectErrors = singleSelectTextErrors.value.some((error) => !!error);
        
        var formData = {
          question: question.value,
          selectedInputType: selectedInputType.value
        }

        var haveError = false;
    
        if (selectedInputType.value == 'Likert Scale') {
          if (!hasLikertScaleErrors && !hasTextareaError) {
            formData.inputOptions = likertScaleText.value;
          } else {
            haveError = true;
          }
        } else if (selectedInputType.value == 'Radio Button') {
          if (!hasRadioErrors && !hasTextareaError) {
            formData.inputOptions = radioButtonText.value;
          } else {
            haveError = true;
          }
        } else if (selectedInputType.value == 'Single Select') {
          if (!hasSingleSelectErrors && !hasTextareaError) {
            formData.inputOptions = singleSelectText.value;
          } else {
            haveError = true;
          }
        } else if (selectedInputType.value == 'Text Field' || selectedInputType.value == 'Number Field') {
          if (hasTextareaError) {
            haveError = true;
          }
        }
        formData.haveError = haveError;
        return formData;
      };

      return {
        v$,
        question,
        likertScaleText,
        radioButtonText,
        singleSelectText,
        isFormValid,
        selectedInputType,
        submitData,
        radioButtonTextErrors,
        likertScaleTextErrors,
        singleSelectTextErrors
      };
    },
    data() {
      return {
        inputTypeSelect: ['Text Field', 'Number Field', 'Likert Scale', 'Radio Button', 'Single Select'],
        optionId: 1,
        draggable: true
      };
    },
    methods: {
      addLikertScaleField() {
        const newId = this.optionId++;
        this.likertScaleText.push({ id: newId, option: '', displayedId: this.likertScaleText.length + 1 });
        this.optionId++;
      },
      addRadioButtonField() {
        const newId = this.optionId++;
        this.radioButtonText.push({ id: newId, option: '', displayedId: this.radioButtonText.length + 1 });
        this.optionId++;
      },
      addSingleSelectField() {
        const newId = this.optionId++;
        this.singleSelectText.push({ id: newId, option: '', displayedId: this.singleSelectText.length + 1 });
        this.optionId++;
      },
      onDataChange() {
        if(this.destroyed == false) {
          let dataToEmit = {
            question: this.question,
            selectedInputType: this.selectedInputType,
            index: this.qnNum,
            originalQnNum: this.originalQnNum,
            id: this.id
          };
          if (this.selectedInputType === 'Likert Scale') {
            dataToEmit.inputOptions = this.likertScaleText;
          } else if (this.selectedInputType === 'Radio Button') {
            dataToEmit.inputOptions = this.radioButtonText;
          } else if (this.selectedInputType === 'Single Select') {
            dataToEmit.inputOptions = this.singleSelectText;
          }
          this.$emit('templateDataChanged', dataToEmit);
        }
      },
      removeOption(id) {
        if (this.selectedInputType === 'Likert Scale') {
          const index = this.likertScaleText.findIndex(option => option.id === id);
          if (index !== -1) {
            this.likertScaleText.splice(index, 1);
          }
        } else if (this.selectedInputType === 'Radio Button') {
          const index = this.radioButtonText.findIndex(option => option.id === id);
          if (index !== -1) {
            this.radioButtonText.splice(index, 1);
          }
        } else if (this.selectedInputType === 'Single Select') { 
          const index = this.singleSelectText.findIndex(option => option.id === id);
          if (index !== -1) {
            this.singleSelectText.splice(index, 1);
          }
        }
      },
    },
    watch: {
      question: {
        handler: 'onDataChange',
        immediate: true,
      },
      selectedInputType: {
        handler: 'onDataChange',
        immediate: true,
      },
      likertScaleText: {
        handler: 'onDataChange',
        immediate: true,
      },
      radioButtonText: {
        handler: 'onDataChange',
        immediate: true,
      },
      singleSelectText: {
        handler: 'onDataChange',
        immediate: true,
      }
    }
}
  
</script>

<style scoped>
.likert-scale-draggable > input, .radio-button-draggable > input, .single-select-draggable > input {
  cursor: grab;
}

.likert-scale-add, .radio-button-add, .single-select-add {
  cursor: pointer;
}

.remove-option {
  margin-left: 10px !important;
}
</style>