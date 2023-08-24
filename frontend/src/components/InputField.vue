<template>
  <input
    v-model="inputValue"
    :type="inputType"
    :placeholder="placeholder"
    autofocus
    class="form-control border-0 shadow-sm px-4 field mb-3"
  />
</template>

<script>
import { ref, watch } from 'vue';

export default {
  props: {
    value: String, // Use 'value' prop for data binding
    type: String,
    placeholder: String,
  },
  setup(props) {
    const inputValue = ref(props.value);
    const inputType = ref(props.type);
    
    // Watch for changes in the prop value and update inputValue accordingly
    watch(() => props.value, (newValue) => {
      inputValue.value = newValue;
    });

    return {
      inputValue,
      inputType,
      
    };
  },
  watch: {
    inputValue(newValue) {
      // console.log('Input value changed:', newValue);
      this.$emit('update:value', newValue);
    },
  },
};
</script>

