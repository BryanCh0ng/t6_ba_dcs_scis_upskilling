<template>
  <div id="contactus">
    <!-- CONTACT US FORM -->
    <div class="container">
      <h2 class="text-center mb-4 pt-5">Contact Us</h2>

      <form @submit.prevent="submitForm">
        <div class="form-group mt-5 mb-4">
          <input-field v-model="subject" type="text" :placeholder="subjectPlaceholder" required/>
        </div>
        <div class="form-group">
          <textarea
            v-model="bodyMessage"
            class="form-control border-0 shadow-sm px-4 field"
            :placeholder="messagePlaceholder"
            style="height: 200px" required
          ></textarea>
        </div>

        <button
          type="submit"
          class="btn btn-block shadow-sm w-100 mt-5 field submitbtn"
          title="Submit"
        >
          Submit
        </button>
      </form>
    </div>
    
    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
  </div>
</template>

<script>
import DefaultModal from "@/components/DefaultModal.vue";
import InputField from "../components/InputField.vue";
import { required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import ContactUsService from "../api/services/contactService.js"
import UserService from "@/api/services/UserService.js";

function showSuccessMessage(vm) {
  vm.title = "Message Sent Successfully";
  vm.message = "Your message has been successfully sent. We appreciate your feedback.";
  vm.showAlert = true;
  vm.buttonType = "success";
}

function showUnsuccessMessage(vm) {
    vm.title = "Message Failed to Send";
    vm.message = "Unfortunately, we were unable to send your message. Please try again later.";
    vm.showAlert = true;
    vm.buttonType = "danger";
}


export default {
  setup() {
    const v$ = useVuelidate(); // Initialize Vuelidate
    return { v$ };
  },

  data() {
    return {
      user_ID: null,
      subject: "",
      bodyMessage: "",
      subjectPlaceholder: "Subject",
      messagePlaceholder: "Message",
      showAlert: false,
      title: "",
      message: "",
      buttonType: "",
    };
  },

  validations() {
    return {
      subject: { required},
      message: { required},
    };
  },
  components: {
    DefaultModal,
    InputField,
  },
  created() {
    document.title = "Contact Us | Upskilling Engagement System";
    this.get_user_id();
  },
  methods: {
    async get_user_id() {
      try {
        const user_ID = await UserService.getUserID()
        this.user_ID = user_ID
        
      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_ID = null;
      }
    },
    async submitForm() {
      // Trigger Vuelidate validation
      this.v$.$touch();

      const formData = {
        user_ID: this.user_ID, 
        msg_Subject: this.subject,
        msg_Body: this.bodyMessage,
        msg_Datetime: new Date().toISOString(), 
      };

      try {
        const response = await ContactUsService.createNewMsg(formData);
       
        if (response.code === 201) {
          showSuccessMessage(this)
        } else {
          showUnsuccessMessage(this)
        }
      } catch (error) {
        console.error('Error submitting form:', error);
      }
    },
    async handleModalClosed(value) {
      this.showAlert = value;

      const role = await UserService.getUserRole(this.user_ID);

      if (role == 'Student') {
        this.$router.push({name: "studentViewCourse"});
      } else if (role == 'Instructor' || role == 'Trainer') {
        this.$router.push({ name: 'instructorTrainerViewProfile' });
      }
      
    },
  },
};
</script>
