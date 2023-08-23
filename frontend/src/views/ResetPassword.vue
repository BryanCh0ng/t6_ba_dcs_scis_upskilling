<template>
  <div class="full-screen-container" id="login">
    <div class="content">
      <div class="row no-gutter">
        <!-- The image half -->
        <div class="col-md-6 d-none d-md-flex bg-image">
          <div class="overlay"></div>
        </div>

        <!-- The content half -->
        <div class="col-md-6 bg-light">
          <div class="login-form d-flex align-items-center py-5">
            <div class="container">
              <div class="row">
                <div class="col-lg-10 col-xl-7 mx-auto">
                  <div class="text-center">
                    <img
                      src="../assets/smulogo.png"
                      title="smu logo"
                      id="logo"
                    />
                  </div>

                  <!-- Error Message -->
                  <error-message :error-message="errorMessage" />

                  <!-- Reset Password Form -->
                  <form @submit.prevent="onSubmit">
                    <div class="input-group password-field mb-3">
                      <input
                        v-model="password"
                        :type="showPassword ? 'text' : 'password'"
                        placeholder="New Password"
                        class="form-control border-0 shadow-sm px-4 field"
                      />
                      <div class="input-group-append">
                        <div class="input-group-text eye-icon-container">
                          <span
                            @click="togglePasswordVisibility"
                            class="eye-icon"
                          >
                            <font-awesome-icon
                              :icon="
                                showPassword
                                  ? ['fas', 'eye']
                                  : ['fas', 'eye-slash']
                              "
                            />
                          </span>
                        </div>
                      </div>
                    </div>

                    <div class="input-group password-field">
                      <input
                        v-model="confirmpassword"
                        :type="showConfirmPassword ? 'text' : 'password'"
                        placeholder="Confirm New Password"
                        class="form-control border-0 shadow-sm px-4 field"
                      />
                      <div class="input-group-append">
                        <div class="input-group-text eye-icon-container">
                          <span
                            @click="toggleConfirmPasswordVisibility"
                            class="eye-icon"
                          >
                            <font-awesome-icon
                              :icon="
                                showConfirmPassword
                                  ? ['fas', 'eye']
                                  : ['fas', 'eye-slash']
                              "
                            />
                          </span>
                        </div>
                      </div>
                    </div>

                    <button
                      type="submit"
                      class="btn btn-block shadow-sm w-100 mt-5 field submitbtn"
                    >
                      Reset Password
                    </button>
                  </form>
                </div>
              </div>
            </div>
            <!-- End -->
          </div>
        </div>
        <!-- End -->
      </div>
    </div>
  </div>
</template>

<script>
import ErrorMessage from "../components/ErrorMessage.vue";
// import InputField from "../components/InputField.vue";
import { required, minLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
// import { axiosClient } from "../api/axiosClient";

export default {
  name: "LoginForm",

  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },
  data() {
    return {
      password: "",
      confirmpassword: "",
      errorMessage: "",
      showPassword: false,
      showConfirmPassword: false,
    };
  },
  validations() {
    return {
      password: { required, minLength: minLength(8) },
      confirmpassword: { required, minLength: minLength(8) },
    };
  },
  components: {
    ErrorMessage,
    // InputField,
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
        // const response = await axiosClient.post("/reset", {
        //   email: this.email,
        // });

        console.log("Reset send");
        // console.log(response.data);
      } catch (error) {
        this.errorMessage = "Reset failed. Please check your credentials.";
        console.log("Reset error:", error.message);
      }
    },
    // Visibility of the password
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPasswordVisibility() {
      this.showConfirmPassword = !this.showConfirmPassword;
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

.login-form,
.image {
  min-height: 100vh;
}

.bg-image {
  background-image: url("../assets/smu_building.jpg");
  background-size: cover;
  background-position: center center;
  position: relative; /* Add this to make the overlay relative to the .bg-image div */
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(
    0,
    0,
    0,
    0.4
  ); /* Adjust the color and opacity as needed */
}

#logo {
  width: 380px;
  margin-bottom: 40px;
}

/* For the visibility of the password */
.password-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: black;
}

.eye-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%; /* Match the height of the input field */
  padding-right: 8px; /* Add spacing between the input and the icon */
  cursor: pointer;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  background-color: white;
  border: 0px;
  width: 40px;
}
</style>
