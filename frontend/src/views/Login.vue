<template>
  <div class="full-screen-container" id="login">
    <div class="content">
      <div class="row no-gutter">
        
        <image-half></image-half>

        <!-- Form content half -->
        <form-container>
          <!-- <template v-slot:logo>
            <img src="../assets/smulogo.png" title="smu logo" id="logo"/>
          </template> -->
            <error-message :error-message="errorMessage" />

            <form @submit.prevent="onSubmit">
              <input-field v-model="email" type="email" placeholder="Email Address"/>
                    
              <password-field :value="password" placeholder="Password" @update:value="password = $event" class="mb-3"/>

              <div>
                <router-link to="/forgotPassword" id="forgotpsd">Forgot password?</router-link>
              </div>

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                Sign In
              </button>

              <p class="text-center mt-2">
                Don't have an account? <router-link to="/register">Sign Up</router-link>
              </p>
            </form>
        </form-container>
        
      </div>
    </div>
    <success-modal :show="showSuccessModal" :message="successMessage" @close="hideSuccessModal"/>
  </div>
</template>

<script>
import ImageHalf from "../components/ImageHalf.vue";
import FormContainer from "../components/CommonFormContainer.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import InputField from "../components/InputField.vue";
import PasswordField from "../components/PasswordField.vue";
import { required, email } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import { axiosClient } from "@/api/axiosClient";
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
      password: "",
      errorMessage: "",
    };
  },
  validations() {
    return {
      email: { required, email },
      password: { required},
    };
  },
  components: {
    FormContainer,
    ErrorMessage,
    InputField,
    ImageHalf,
    PasswordField,
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.errorMessage = ""; // Reset error message

      // Check for empty fields
      if (!this.email || !this.password) {
        this.errorMessage = "Please ensure all fields are filled.";
        return;
      }
      
      if (this.v$.$invalid) {
        this.errorMessage = "Please fix the validation errors.";
        return;
      }

      this.performLogin();
    },

    async performLogin() {
      try {
        const response = await axiosClient.post("/login/login", {
          email: this.email,
          password: this.password
        })
        
        const role = await axiosClient.get("/login/get_role")
        console.log(role.data)

        console.log(response);
      } catch (error) {
        this.errorMessage = "Login failed. Please check your credentials.";
        console.log("Login error:", error.message);
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
  overflow: hidden;
}

#forgotpsd {
  float: right;
}
</style>
