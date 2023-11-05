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

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn" title="Sign Up">
                Sign Up
              </button>

              <p class="text-center mt-2">
                Already have an account? <router-link to="/">Sign In</router-link>
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
import SuccessModal from "../components/SuccessModal.vue";
import FormContainer from "../components/CommonFormContainer.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import InputField from "../components/InputField.vue";
import { required, email } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";

export default {
  name: "RegistrationForm",

  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      email: "",
      errorMessage: "",
      showSuccessModal: false,
      successMessage: "Registration link has been sent to your email."
    };
  },
  validations() {
    return {
      email: { required, email },
    };
  },
  components: {
    ImageHalf,
    SuccessModal,
    FormContainer,
    ErrorMessage,
    InputField,
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      // Reset error message
      this.errorMessage = "";

      // Check for required fields
      if (!this.email) {
        this.errorMessage = "Please ensure all fields are filled.";
        return;
      }

      this.sendRegLink();
    },
    async sendRegLink() {
      try {
        const response = await UserService.verifyEmail(this.email)
        this.showSuccessModal = true;
        console.log(response);
      } catch (error) {
        this.errorMessage = "Sent Registration failed. Please check your credentials.";
        console.log("Sent Registration Link error:", error.message);
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
  overflow: hidden;
}
</style>
