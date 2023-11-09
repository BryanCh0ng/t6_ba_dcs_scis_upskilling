<template>
  <div class="form-group row">
    <label v-if="qnNum !== undefined" class="mb-1">{{ qnNum }}. {{ label }}</label>
    <label v-else class="mb-1">{{ label }}</label>
    <select class="form-control" :value="sOption" v-model="selectedOption" :id="id">
      <option value="" disabled selected>{{ label }}</option>
      <option :disabled="disabled" v-for="option in options" :key="option.id" :value="option.position">{{ option.option }}</option>
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
      }
    },
    watch: {
      selectedOption(newValue) {
        this.$emit('input', {value: newValue, key: this.qnNum-1});
      },
    },
  };
  </script>