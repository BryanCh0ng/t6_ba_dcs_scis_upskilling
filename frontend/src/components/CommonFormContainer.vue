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
