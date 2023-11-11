<template>
  <div class="full-screen-container" id="login">
    <div class="onboard">
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

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn" title="Request password reset link">
                Request reset link
              </button>
              <p class="text-center mt-2">
                Back to <router-link to="/">Sign In</router-link>
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
import FormContainer from "../components/RegistrationPasswordContainer.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import InputField from "../components/InputField.vue";
import SuccessModal from "../components/SuccessModal.vue";
import { required, email } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";

export default {
  name: "ForgotPassword",

  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      email: "",
      errorMessage: "",
      showSuccessModal: false,
      successMessage: "Reset link has been sent to your email."
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
    SuccessModal,
    ImageHalf,
    FormContainer
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.errorMessage = ""; // Reset error message


      // Check for empty fields
      if (!this.email) {
        this.errorMessage = "Please ensure the email field is filled and is valid.";
        return;
      }
      
      if (this.v$.$invalid) {
        this.errorMessage = "Please fix the validation errors.";
        return;
      }

      this.sendResetLink();
    },

    async sendResetLink() {
      try {
        // Will need to update the flask api endpoint
        // Send login request
        const response = await UserService.forgotPassword(this.email)
        if (response.code === 200) {
          this.showSuccessModal = true;
        }
        
      } catch (error) {
        this.errorMessage = "Sent reset link failed. Please check your credentials.";
        console.log("Reset error:", error.request.response);
      }
    },
    hideSuccessModal() {
      this.showSuccessModal = false;
      this.$router.push('/');
    },

  },
};
</script>

<style>
.onboard {
  padding: 0px;
  font-size: 15px;
}


body {
  overflow:hidden;
}
</style>
