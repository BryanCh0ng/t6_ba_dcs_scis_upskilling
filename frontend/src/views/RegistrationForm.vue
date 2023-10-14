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

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn">
                Sign Up
              </button>

              <p class="text-center mt-2">
                Already have an account?<router-link to="/">Sign In</router-link>
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
import DropdownField from "../components/DropdownField.vue";
import InputField from "../components/InputField.vue";
import PasswordField from "../components/PasswordField.vue";
import { required, email, minLength } from "@vuelidate/validators";
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
      role: "",
      fullName: "",
      email: "",
      password: "",
      confirmpassword: "",
      organizationName: "",
      alumni: "",
      errorMessage: "",
      showSuccessModal: false,
      successMessage: "Your account has been successfully created."
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
    SuccessModal,
    FormContainer,
    ErrorMessage,
    DropdownField,
    InputField,
    PasswordField,
  },
  methods: {
    onSubmit() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      // Display the current form data for debugging
      // console.log("Form Data:", {
      //   role: this.role,
      //   fullName: this.fullName,
      //   email: this.email,
      //   password: this.password,
      //   confirmpassword: this.confirmpassword,
      //   organizationName: this.organizationName,
      //   alumni: this.alumni,
      // });

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
        console.log(userData)
        const response = await UserService.register(userData)
        // const response = await axiosClient.post("/user/register", {
        //   role: this.role,
        //   fullName: this.fullName,
        //   email: this.email,
        //   password: this.password,
        //   confirmpassword: this.confirmpassword,
        //   organizationName: this.organizationName,
        //   alumni: this.alumni,
        // });
        console.log(response)
        this.showSuccessModal = true;
      } catch (error) {
        this.errorMessage = "Register failed. Please check your credentials.";
        console.log("Register error:", error.request.response);
      }
    },
    clearPlaceholder() {
      if (this.role === "") {
        this.role = ""; // Clear the placeholder value when the user interacts
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
