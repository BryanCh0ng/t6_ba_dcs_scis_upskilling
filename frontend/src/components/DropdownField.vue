<template>
  <div class="form-group mb-3 dropdown-field">
    <select v-model="selectedValue" class="form-select border-0 shadow-sm px-4 field">
      <option value="" disabled selected hidden>{{ defaultPlaceholder }}</option>
      <slot></slot>
    </select>
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  props: {
    modelValue: String, 
    defaultPlaceholder: String,
  },
  setup(props, { emit }) {
    const selectedValue = ref(props.modelValue || '');

    watch(
      () => props.modelValue,
      (newValue) => {
        selectedValue.value = newValue;
      }
    );

    watch(selectedValue, (newValue) => {
      emit('update:modelValue', newValue);
    });

    return {
      selectedValue,
    };
  },
};
</script>

<style scoped>
.dropdown-field {
  position: relative;
}
</style>
