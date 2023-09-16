<template>
  <div class="form-group row">
    <label class="mb-1">{{ label }}</label>
    <select class="form-control" v-model="selectedOption" :id="id">
      <option value="" disabled selected>{{ label }}</option>
      <option v-for="option in options" :key="option.id" :value="option.id">{{ option.option }}</option>
    </select>
  </div>
</template>
    
  <script>
  export default {
    props: {
      label: String,
      id: Number,
      options: Array
    },
    data() {
      return {
        selectedOption: ""
      }
    }
  };
  </script>