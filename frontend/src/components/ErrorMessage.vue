<template>
    <div v-if="errorMessage" class="error-message text-danger" id="errorMsg">
      {{ errorMessage }}
    </div>
  </template>
  
  <script>
  export default {
    props: {
      errorMessage: String,
    },
  };
  </script>
  
  <style scoped>
  #errorMsg {
    text-align: center;
    margin-bottom: 40px;
  }
  </style>