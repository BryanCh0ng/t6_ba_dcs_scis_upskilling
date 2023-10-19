<template>
    <div>
      <label v-if="qnNum !== undefined" class="mb-1">{{ qnNum }}. {{ label }}</label>
      <label v-else class="mb-1">{{ label }}</label>
      <div v-for="option in options" :key="option.id">
        <input
        type="radio"
        :name="label"
        :value="option.option"
        :disabled="disabled"
        :checked="sOption === option.option"
        v-model="selectedOption"
      />{{ option.option }}
      </div>
    </div>
  </template>
    
  <script>
  export default {
    props: {
      label: String,
      id: Number,
      options: Array,
      qnNum: Number,
      value: String,
      disabled: {
        type: Boolean,
        default: false,
      },
      sOption: String
    },
    data() {
    return {
      selectedOption: this.value || '', 
      };
    },
    watch: {
      selectedOption(newValue) {
        this.$emit('input', {value: newValue, key: this.qnNum-1});
      }
    }
  };
  </script>

