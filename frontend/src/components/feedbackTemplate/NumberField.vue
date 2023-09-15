<template>
  <div class="form-group row">
    <label class="mb-1">{{ label }}</label>
    <input type="text" :number="id" class="form-control" placeholder="Number Field">
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