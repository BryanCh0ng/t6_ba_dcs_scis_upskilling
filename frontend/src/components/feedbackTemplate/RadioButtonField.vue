<template>
    <div>
      <label for="">{{ label }}</label>
      <div v-for="option in options" :key="option.id">
        <input type="radio" :name="label" :value="option.id"> {{ option.option }}
      </div>
    </div>
  </template>
    
  <script>
  export default {
    props: {
      label: String,
      id: Number,
      options: Array
    },
  };
  </script>