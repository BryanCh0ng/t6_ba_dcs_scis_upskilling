<template>
  <div class="form-group row">
    <label class="mb-1">{{ qnNum }}. {{ label }}</label>
    <select class="form-control" v-model="selectedOption" :id="id">
      <option value="" disabled selected>{{ label }}</option>
      <option v-for="option in options" :key="option.id" :value="option.option">{{ option.option }}</option>
    </select>
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
      }
    },
    watch: {
      selectedOption(newValue) {
        this.$emit('input', {value: newValue, key: this.qnNum-1});
      },
    },
  };
  </script>