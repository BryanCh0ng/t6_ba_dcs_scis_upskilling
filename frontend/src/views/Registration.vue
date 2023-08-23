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
            <!-- Login Form -->
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

                  <error-message :error-message="errorMessage" />

                  <form @submit.prevent="onSubmit">
                    <dropdown-field
                      v-model="role"
                      :default-placeholder="'Select a Role'"
                    >
                      <option value="Student">Student</option>
                      <option value="Instructor">Instructor</option>
                      <option value="Trainer">External Trainer</option>
                    </dropdown-field>

                    <input-field
                      v-model="fullName"
                      type="text"
                      placeholder="Full Name"
                    />

                    <input-field
                      v-model="email"
                      type="email"
                      placeholder="Email Address"
                    />

                    <div v-if="role === 'Trainer'">
                      <input-field
                        v-model="organizationName"
                        type="text"
                        placeholder="Organization Name"
                      />
                      <dropdown-field
                        v-model="alumni"
                        :default-placeholder="'Are you an alumni?'"
                      >
                        <option value="1">Yes</option>
                        <option value="0">No</option>
                      </dropdown-field>
                    </div>

                    <div>
                      <div class="input-group password-field mb-3">
                        <input
                          v-model="password"
                          :type="showPassword ? 'text' : 'password'"
                          placeholder="Password"
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
                      Sign Up
                    </button>
                    <p class="text-center mt-2">
                      Already have an account?
                      <router-link to="/login">Sign In</router-link>
                    </p>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ErrorMessage from "../components/ErrorMessage.vue";
import DropdownField from "../components/DropdownField.vue";
import InputField from "../components/InputField.vue";
import { required, email, minLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
// import { axiosClient } from "../api/axiosClient";

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
      showPassword: false,
      showConfirmPassword: false,
      errorMessage: "",
    };
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
    ErrorMessage,
    DropdownField,
    InputField,
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
      //   organizationName: this.organizationName,
      //   alumni: this.alumni,
      // });

      // Reset error message
      this.errorMessage = "";

      // Check for required fields
      if (!this.role || !this.fullName || !this.email || !this.password) {
        this.errorMessage = "Please ensure all fields are filled.";
        return;
      }

      // Additional validation for Trainer role - required fields
      if (this.role === "Trainer" && (!this.organizationName || !this.alumni)) {
        this.errorMessage = "Please ensure all fields are filled.";
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

      this.performRegister();
    },
    async performRegister() {
      try {
        // Will need to update the flask api endpoint
        // Send login request
        // const response = await axiosClient.post("/login", {
        //   email: this.email,
        //   password: this.password,
        // });

        console.log("Register successful");
        // console.log(response.data);
      } catch (error) {
        this.errorMessage = "Register failed. Please check your credentials.";
        console.log("Register error:", error.message);
      }
    },
    clearPlaceholder() {
      if (this.role === "") {
        this.role = ""; // Clear the placeholder value when the user interacts
      }
    },
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
