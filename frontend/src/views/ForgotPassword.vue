<template>
  <div class="full-screen-container" id="login">
    <div class="content">
      <div class="row no-gutter">
        <!-- The image half -->
        <div class="col-md-6 d-none d-md-flex bg-image">
          <div class="overlay"></div>
        </div>

        <!-- The content half -->
        <div class="col-md-6 bg-light">
          <div class="login-form d-flex align-items-center py-5">
            
            <div class="container">
              <div class="row">
                <div class="col-lg-10 col-xl-7 mx-auto">
                  <div class="text-center">
                    <img src="../assets/smulogo.png" title="smu logo" id="logo"/>
                  </div>

                  <!-- Error Message -->
                  <error-message :error-message="errorMessage" />

                  <!-- Reset Password Form -->
                  <form @submit.prevent="onSubmit">
                    <input-field
                      v-model="email"
                      type="email"
                      placeholder="Email Address"
                    />

                    <button
                      type="submit"
                      class="btn btn-block shadow-sm w-100 mt-5 field submitbtn"
                    >Reset Password
                    </button>
                    <p class="text-center mt-2">
                      Back to
                      <router-link to="/login">Sign In</router-link>
                    </p>
                  </form>
                </div>
              </div>
            </div>
            <!-- End -->
          </div>
        </div>
        <!-- End -->
      </div>
    </div>
  </div>
</template>

<script>
import ErrorMessage from "../components/ErrorMessage.vue";
import InputField from "../components/InputField.vue";
import { required, email } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
// import { axiosClient } from "../api/axiosClient";

export default {
  name: "LoginForm",

  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      email: "",
      errorMessage: "",
    };
  },

  validations() {
    return {
      email: { required, email },
    };
  },
  components: {
    ErrorMessage,
    InputField,
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.errorMessage = ""; // Reset error message

      // Check for empty fields
      if (!this.email) {
        this.errorMessage = "Please ensure the email field is filled.";
        return;
      }
      
      if (this.v$.$invalid) {
        this.errorMessage = "Please fix the validation errors.";
        return;
      }

      this.performReset();
    },

    async performReset() {
      try {
        // Will need to update the flask api endpoint
        // Send login request
        // const response = await axiosClient.post("/reset", {
        //   email: this.email,
        // });

        console.log("Reset send");
        // console.log(response.data);
      } catch (error) {
        this.errorMessage = "Reset failed. Please check your credentials.";
        console.log("Reset error:", error.message);
      }
    },

  },
};
</script>

<style>
.content {
  padding: 0px;
  font-size: 15px;
}

body {
  overflow:hidden;
}

.login-form,
.image {
  min-height: 100vh;
}

.bg-image {
  background-image: url("../assets/smu_building.jpg");
  background-size: cover;
  background-position: center center;
  position: relative; /* Add this to make the overlay relative to the .bg-image div */
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4); /* Adjust the color and opacity as needed */
}

#logo {
  width: 380px;
  margin-bottom: 40px;
}
</style>
