<template>
  <div v-if="errorMessage" class="error-message text-danger" id="errorMsg">
    {{ errorMessage }}

    <router-link to="/register" v-if="errorMessage === 'Please sign up with your SMU email address.'">
      Go to Sign Up
    </router-link>
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
