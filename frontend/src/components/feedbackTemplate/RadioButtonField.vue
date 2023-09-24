<template>
    <div>
      <label for="">{{ qnNum }}. {{ label }}</label>
      <div v-for="option in options" :key="option.id">
        <input
        type="radio"
        :name="label"
        :value="option.option"
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
      value: String
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

