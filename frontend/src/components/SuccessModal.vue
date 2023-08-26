<template>
    <div v-if="show" class="modal-backdrop">
      <div class="modal-content">
        <p>{{ message }}</p>
        <button @click="hide" class="btn btn-secondary close-btn">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SuccessModal",
  
    props: {
      show: Boolean,
      message: String,
    },
    methods: {
      hide() {
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-content {
    width: 40%;
    height: 15%;
  }
  
  .close-btn {
    position: absolute;
    bottom: 25px;
    right: 20px;
    width: 150px;
  }
  
  @media (max-width: 768px) {
    .modal-content {
      width: 60%;
      height: 18%;
    }
  }
  </style>