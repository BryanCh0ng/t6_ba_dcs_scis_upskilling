<template>
  <div class="full-screen-container" id="login">
    <div class="onboard">
      <div class="row no-gutter">
        
        <image-half></image-half>

        <form-container>

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
    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
  </div>
</template>

<script>
import ImageHalf from "../components/ImageHalf.vue";
import FormContainer from "../components/CommonFormContainer.vue";
import InputField from "../components/InputField.vue";
import { required, email } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";
import DefaultModal from "@/components/DefaultModal.vue";

function showSuccessMessage(vm) {
  vm.title = "Registration Link Sent Successfully";
  vm.message = "Registration link has been sent successfully. Please check your email";
  vm.showAlert = true;
  vm.buttonType = "success";
}

function showUnsuccessMessage(vm) {
    vm.title = "Registration Link Sent Unsuccessfully";
    vm.message = "Sent registration link failed. Please check your credentials.";
    vm.showAlert = true;
    vm.buttonType = "danger";
}

export default {
  name: "RegistrationForm",

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
      buttonType: ""
    };
  },
  validations() {
    return {
      email: { required, email },
    };
  },
  components: {
    ImageHalf,
    FormContainer,
    InputField,
    DefaultModal
  },
  created() {
    document.title = "Sign Up | Upskilling Engagement System";
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      this.sendRegLink();
    },
    async sendRegLink() {
      try {
        const response = await UserService.verifyEmail(this.email)
        if (response.code === 200) {
          showSuccessMessage(this)
        } else {
          showUnsuccessMessage(this)
        }
        
      } catch (error) {
        showUnsuccessMessage(this)
        console.log("Sent Registration Link error:", error.message);
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
