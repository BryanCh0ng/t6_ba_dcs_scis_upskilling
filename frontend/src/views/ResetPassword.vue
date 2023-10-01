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
              <div class="input-group password-field mb-3">
                <password-field :value="password" placeholder="Password" @update:value="password = $event" class="mb-3"/>

                <password-field :value="confirmpassword" placeholder="Confirm Password" @update:value="confirmpassword = $event"/>
              </div>

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                Reset Password
              </button>
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
import PasswordField from "../components/PasswordField.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import SuccessModal from "../components/SuccessModal.vue";
import { required, minLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";


export default {
  name: "ResetPassword",

  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },
  data() {
    return {
      password: "",
      confirmpassword: "",
      email: "",
      errorMessage: "",
      showSuccessModal: false,
      successMessage: "You have reset your password successfully."
    };
  },
  created() {
    this.email = this.$route.query.email
  },
  validations() {
    return {
      password: { required, minLength: minLength(8) },
      confirmpassword: { required, minLength: minLength(8) },
    };
  },
  components: {
    ErrorMessage,
    SuccessModal,
    PasswordField,
    ImageHalf,
    FormContainer
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.errorMessage = ""; // Reset error message

      console.log("Form Data:", {
        password: this.password,
        confirmpassword: this.confirmpassword,
      });

      // Check for empty fields
      if (!this.password || !this.confirmpassword) {
        this.errorMessage = "Please ensure the email field is filled.";
        return;
      }

      // Check password length
      if (this.password.length < 8) {
        this.errorMessage = "Password must be at least 8 characters long.";
        return;
      }

      // Check password complexity (letters, numbers, special characters)
      const passwordRegex =
        /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
      if (!passwordRegex.test(this.password)) {
        this.errorMessage =
          "Password must contain at least one letter, one number, and one special character.";
        return;
      }

      if (this.confirmpassword != this.password) {
        this.errorMessage = "Password and Confirm Password do not match.";
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
        console.log(this.email)
        const response = await UserService.resetPassword(this.password, this.confirmpassword, this.email)
       

        this.showSuccessModal = true;
        console.log(response.data);
      } catch (error) {
        this.errorMessage = "Reset failed. Please check your credentials.";
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
.content {
  padding: 0px;
  font-size: 15px;
}

body {
  overflow: hidden;
}

</style>
