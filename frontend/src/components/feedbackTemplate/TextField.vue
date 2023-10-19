<template>
  <div class="form-group row">
    <label v-if="qnNum !== undefined" class="mb-1">{{ qnNum }}. {{ label }}</label>
    <label v-else class="mb-1">{{ label }}</label>
    <input :placeholder="placeholder" :disabled="disabled" type="text" :class="id" class="form-control" v-model="userInput"> 
  </div>
</template>
  
<script>
export default {
  props: {
    label: String,
    id: Number,
    qnNum: Number,
    disabled: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: 'Enter Text',
    },
  },
  data() {
    return {
      userInput: this.value || ''
    };
  },
  watch: {
    userInput(newValue) {
      this.$emit('input', {value: newValue, key: this.qnNum-1});
    },
  },
};
</script>