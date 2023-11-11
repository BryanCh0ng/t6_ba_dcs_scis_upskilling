<template>
  <div class="full-screen-container" id="login">
    <div class="onboard">
      <div class="row no-gutter">
        
        <image-half></image-half>

        <form-container>

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
    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
  </div>
</template>

<script>
import ImageHalf from "../components/ImageHalf.vue";
import FormContainer from "../components/RegistrationPasswordContainer.vue";
import InputField from "../components/InputField.vue";
import { required, email } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";
import DefaultModal from "@/components/DefaultModal.vue";

function showSuccessMessage(vm) {
  vm.title = "Reset Password Link Successfully";
  vm.message = "Reset password link has been sent successfully. Please check your email.";
  vm.showAlert = true;
  vm.buttonType = "success";
}

function showUnsuccessMessage(vm) {
    vm.title = "Reset Password Link Unsuccessfully";
    vm.message = "Sent reset password link failed. Please check your credentials.";
    vm.showAlert = true;
    vm.buttonType = "danger";
}

export default {
  name: "ForgotPassword",

  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      email: "",
      showAlert: false,
      title: "",
      message: "",
      buttonType: "",
    };
  },

  validations() {
    return {
      email: { required, email },
    };
  },
  components: {
    InputField,
    ImageHalf,
    FormContainer,
    DefaultModal
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.sendResetLink();
    },

    async sendResetLink() {
      try {
        console.log(this.email)
        const response = await UserService.forgotPassword(this.email)
        
        if (response.code === 200) {
          showSuccessMessage(this)
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
  overflow:hidden;
}
</style>
