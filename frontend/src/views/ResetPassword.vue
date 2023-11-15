<template>
  <div class="full-screen-container" id="login">
    <div class="onboard">
      <div class="row no-gutter">
        
        <image-half></image-half>

        <form-container>
            <error-message :error-message="errorMessage" />

            <form @submit.prevent="onSubmit">
              <div class="input-group password-field mb-3">
                <password-field :value="password" placeholder="Password" @update:value="password = $event" class="mb-3"/>

                <password-field :value="confirmpassword" placeholder="Confirm Password" @update:value="confirmpassword = $event"/>
              </div>

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn" title="Reset Password">
                Reset Password
              </button>
            </form>
        </form-container>
        
      </div>
    </div>
    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
  </div>
</template>

<script>
import ImageHalf from "../components/ImageHalf.vue";
import FormContainer from "../components/RegistrationPasswordContainer.vue";
import PasswordField from "../components/PasswordField.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import { required, minLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";
import DefaultModal from "@/components/DefaultModal.vue";

function showSuccessMessage(vm) {
  vm.title = "Reset Password Successfully";
  vm.message = "Reset password link has been sent successfully. Please check your email.";
  vm.showAlert = true;
  vm.buttonType = "success";
}

function showUnsuccessMessage(vm) {
    vm.title = "Reset Password Unsuccessfully";
    vm.message = "Reset password unsucessfully. Please check your credentials.";
    vm.showAlert = true;
    vm.buttonType = "danger";
}

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
      showAlert: false,
      title: "",
      message: "",
      buttonType: "",
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
    PasswordField,
    ImageHalf,
    FormContainer,
    DefaultModal
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.errorMessage = ""; // Reset error message

      // Check for empty fields
      if (!this.password || !this.confirmpassword) {
        this.errorMessage = "Please ensure the email field is filled.";
        return;
      }

      // Check password complexity (letters, numbers, special characters)
       const passwordRegex =
        /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
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
        
        const response = await UserService.resetPassword(this.password, this.confirmpassword, this.email)
        if (response.code === 200) {
          showSuccessMessage(this)
        } else {
          showUnsuccessMessage(this)
        }

        
      } catch (error) {
        showUnsuccessMessage(this)
        console.log("Reset error:", error.request.response);
      }
    },
    async handleModalClosed(value) {
      this.showAlert = value;

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
