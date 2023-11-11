<template>
  <div class="full-screen-container" id="login">
    <div class="onboard">
      <div class="row no-gutter">
        
        <image-half></image-half>

        <!-- Form content half -->
        <form-container>
         
            <error-message :error-message="errorMessage" />

            <form @submit.prevent="onSubmit">
              <dropdown-field v-model="role" :default-placeholder="'Select a Role'">
                <option value="Student">Student</option>
                <option value="Instructor">Instructor</option>
                <option value="Trainer">External Trainer</option>
              </dropdown-field>

              <input-field v-model="fullName" type="text" placeholder="Full Name"/>

              <!-- <input-field v-model="email" type="email" placeholder="Email Address" readonly/> -->

              <div v-if="role === 'Trainer'">
                <input-field v-model="organizationName" type="text" placeholder="Organization Name"/>

                <dropdown-field v-model="alumni" :default-placeholder="'Are you an alumni?'">
                  <option value="1">Yes</option>
                  <option value="0">No</option>
                </dropdown-field>
              </div>

              <password-field :value="password" placeholder="Password" @update:value="password = $event" class="mb-3"/>

              <password-field :value="confirmpassword" placeholder="Confirm Password" @update:value="confirmpassword = $event"/>

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn" title="Sign Up">
                Sign Up
              </button>

              <p class="text-center mt-2">
                Already have an account?<router-link to="/">Sign In</router-link>
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
import DefaultModal from "@/components/DefaultModal.vue";
import FormContainer from "../components/CommonFormContainer.vue";
import ErrorMessage from "../components/ErrorMessage.vue";
import DropdownField from "../components/DropdownField.vue";
import InputField from "../components/InputField.vue";
import PasswordField from "../components/PasswordField.vue";
import { required, email, minLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import UserService from "@/api/services/UserService.js";

function showSuccessMessage(vm) {
  vm.title = "Registered Successfully";
  vm.message = "You have been successfully registered. You can now proceed to log into your account!";
  vm.showAlert = true;
  vm.buttonType = "success";
}

function showUnsuccessMessage(vm) {
    vm.title = "Registered Unsuccessfully";
    vm.message = "We're sorry, but your registration could not be completed at this time. Please double-check your information and try again.";
    vm.showAlert = true;
    vm.buttonType = "danger";
}

export default {
  name: "RegistrationForm",

  setup() {
    const v$ = useVuelidate(); 
    return { v$ };
  },

  data() {
    return {
      role: "",
      fullName: "",
      email: "",
      password: "",
      confirmpassword: "",
      organizationName: "",
      alumni: "",
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
      role: { required },
      fullName: { required },
      email: { required, email },
      password: { required, minLength: minLength(8) },
      confirmpassword: { required, minLength: minLength(8) },
    };
  },
  components: {
    ImageHalf,
    FormContainer,
    ErrorMessage,
    DropdownField,
    InputField,
    PasswordField,
    DefaultModal
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      // Reset error message
      this.errorMessage = "";

      // Check for required fields
      if (!this.role || !this.fullName || !this.email || !this.password || !this.confirmpassword) {
        this.errorMessage = "Please ensure all fields are filled.";
        return;
      }

      const smuStudentEmailPattern = /^[\w.-]+@(?:[a-zA-Z]+\.)?smu\.edu\.sg$/i;
      if (this.role === "Student") {
        if (!smuStudentEmailPattern.test(this.email)) {
          this.errorMessage = "Please sign up with your SMU email address."
          return;
        }
      }

      const smuEmailPattern = /^[\w.-]+@smu\.edu\.sg$/i;
      if (this.role === "Instructor") {
        if (!smuEmailPattern.test(this.email)) {
          this.errorMessage = "Please sign up with your SMU email address."
          return;
        }
      }

      // Additional validation for Trainer role - required fields
      if (this.role === "Trainer" && (!this.organizationName || !this.alumni)) {
        this.errorMessage = "Please ensure all fields are filled.";
        return;
      }

      // Check password complexity (letters, numbers, special characters)
      const passwordRegex =
        /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
      if (!passwordRegex.test(this.password)) {
        this.errorMessage =
          "Password must contain at least one uppercase, one lowercase, one number, one special character and at least 8 characters long.";
        return;
      }

      if (this.confirmpassword !== this.password) {
        this.errorMessage = "Password and Confirm Password do not match.";
        return;
      }

      this.performRegister();
    },
    async performRegister() {
      try {
        const userData = {
            role: this.role,
            fullName: this.fullName,
            email: this.email,
            password: this.password,
            confirmpassword: this.confirmpassword,
            organizationName: this.organizationName,
            alumni: this.alumni,
        }
        
        const response = await UserService.register(userData)
        console.log(response)
        if (response.code === 200) {
          showSuccessMessage(this)
        } else {
          showUnsuccessMessage(this)
        }
        
      } catch (error) {
        showUnsuccessMessage(this)
        console.log("Register error:", error.request.response);
      }
    },
    clearPlaceholder() {
      if (this.role === "") {
        this.role = ""; // Clear the placeholder value when the user interacts
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
