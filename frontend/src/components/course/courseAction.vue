<template>
  <button class="btn btn-blue-green hop-on text-light font-weight-bold text-nowrap" v-if="action == 'hopOn'">Hop On</button>
  <button class="btn btn-warning shoutout text-light font-weight-bold text-nowrap" v-else-if="action == 'shoutOut'">Shout Out</button>
  <button class="btn btn-edit edit text-light font-weight-bold text-nowrap" v-else-if="action == 'edit'">Edit</button>
</template>
  
<script>
export default {
  props: {
    action: String,
  }
};
</script>
  