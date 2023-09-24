<template>
  <div class="form-group row">
    <label class="mb-1">{{ qnNum }}. {{ label }}</label>
    <input type="text" :class="id" class="form-control" v-model="userInput" placeholder="Enter Text"> 
  </div>
</template>
  
<script>
export default {
  props: {
    label: String,
    id: Number,
    qnNum: Number
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