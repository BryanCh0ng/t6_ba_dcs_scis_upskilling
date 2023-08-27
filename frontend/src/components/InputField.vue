<template>
  <div>
    <input
      v-model="inputValue"
      :type="inputType"
      :placeholder="placeholder"
      autofocus
      :class="{ 'form-control': true, 'border-0': true, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': hasError }"
    />
    <div v-if="hasError" class="text-danger">
      <span v-for="error in errors" :key="error">{{ error }}</span>
    </div>
  </div>
  </template>
  
  <script>
  import { ref, watch } from 'vue';
  
  export default {
    props: {
      value: String, // Use 'value' prop for data binding
      type: String,
      placeholder: String,
      errors: Array, // Pass errors from parent
    },
    setup(props, { emit }) {
      const inputValue = ref(props.value);
      const inputType = ref(props.type);
      const hasError = ref(false);
      const errorMessage = ref('');
      
      // Watch for changes in the prop value and update inputValue accordingly
      watch(() => props.value, (newValue) => {
        inputValue.value = newValue;
      });

      watch(inputValue, (newValue) => {
        emit('update:value', newValue);
      });

      // Watch for changes in errors and update hasError accordingly
      watch(() => props.errors, (newErrors) => {
        hasError.value = newErrors && newErrors.length > 0;
        errorMessage.value = hasError.value ? newErrors[0] : '';
      });

  
      return {
        inputValue,
        inputType,
        hasError,
        errorMessage,
      };
    },
  };
  </script>