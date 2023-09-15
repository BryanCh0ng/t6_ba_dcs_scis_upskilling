<template>
  <div class="form-group row">
    <label class="mb-1">{{ label }}</label>
    <input type="text" :class="id" class="form-control" placeholder="Text Field">
  </div>
</template>
  
<script>
export default {
  props: {
    label: String,
    id: Number
  },
};
</script>