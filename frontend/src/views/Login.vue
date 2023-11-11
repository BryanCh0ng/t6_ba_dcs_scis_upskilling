<template>
  <div class="full-screen-container" id="login">
    <div class="onboard">
      <div class="row no-gutter">
        
        <image-half></image-half>

        <!-- Form content half -->
        <form-container>
            <error-message :error-message="errorMessage" />

            <form @submit.prevent="onSubmit">
              <input-field v-model="email" type="email" placeholder="Email Address"/>
                    
              <password-field :value="password" placeholder="Password" @update:value="password = $event" class="mb-3"/>

              <div>
                <router-link to="/forgotPassword" id="forgotpsd">Forgot password?</router-link>
              </div>

              <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn" title="Sign In">
                Sign In
              </button>

              <p class="text-center mt-2">
                Don't have an account? <router-link to="/register" title="Sign Up">Sign Up</router-link>
              </p>
            </form>
        </form-container>
        
      </div>
    </div>
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
import { useRouter } from 'vue-router';
import UserService from "@/api/services/UserService.js";

export default {
  name: "LoginForm",

  setup() {
    const v$ = useVuelidate(); 
    const router = useRouter(); 
    return { v$, router };
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
      this.v$.$touch();

      this.errorMessage = ""; 

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
        const response = await UserService.login(this.email,this.password)
        if (response.code === 200) {
          let userRole = await UserService.getUserRole()
          if (userRole === 'Student') {
            this.router.push('/studentViewRecommendations')
          } else if (userRole === 'Instructor' || userRole === 'Trainer') {
            this.router.push('/instructorTrainerViewVotingCampaign')
          } else if (userRole === 'Admin') {
            this.router.push('/adminViewCourse')
          }
        }

      } catch (error) {
        this.errorMessage = "Login failed. Please check your credentials.";
        console.log("Login error:", error.message);
      }
    },
  },
};
</script>

<style scoped>
.onboard {
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
