<template>
  <div class="col-md-6 bg-light">
    <div class="login-form d-flex align-items-center py-5">
      <div class="container">
        <div class="row">
          <div class="col-lg-10 col-xl-7 mx-auto">
            <div class="text-center">
              <slot name="logo">
                <img src="../assets/smulogo.png" title="smu logo" id="logo"/>
              </slot>
              <div class="login_text mb-3 text-start">
                <p class="lh-lg">
                  <strong>SMU Student & Instructor (from SMU): </strong> Sign in with your SMU email address
                  <br>
                  <strong>External Trainer: </strong> Sign in with your organization email address
                  <br><br>
                </p>
              </div>
            </div>

            <!-- Slot for form content -->
            <slot></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FormContainer",
};
</script>

<style scoped>
.login-form {
  min-height: 100vh;
}

#logo {
  width: 380px;
  margin-bottom: 40px;
}
</style>
