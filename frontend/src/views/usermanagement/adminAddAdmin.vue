<template>
    <div id="addadmin">
        <div class="container mt-5 pt-5">

            <h2 class="text-center">Add Admin</h2>

            <form @submit.prevent="onSubmit">
                <!--Email-->
                <div class="form-group mt-5 mb-4">
                    <input v-model="formData.emailAddress" type="email" placeholder="Email Address" required autofocus
                        :class="{ 'form-control': true, 'border-0': !v$?.formData.emailAddress?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.emailAddress?.$error }" />
                    <div v-if="v$?.formData.emailAddress?.$error" class="text-danger">
                        <span v-for="error in v$?.formData.emailAddress?.$errors" :key="error.$uid">{{ error.$message}}</span>
                    </div>
                </div>
                <!--Full Name-->
                <div class="form-group mt-5 mb-4">
                    <input v-model="formData.fullName" type="text" placeholder="Full Name" required autofocus
                        :class="{ 'form-control': true, 'border-0': !v$?.formData.fullName?.$error, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': v$?.formData.fullName?.$error }" />
                    <div v-if="v$?.formData.fullName?.$error" class="text-danger">
                        <span v-for="error in v$?.formData.fullName?.$errors" :key="error.$uid">{{ error.$message}}</span>
                    </div>
                </div>
                
                <button type="submit" class="btn btn-block shadow-sm w-100 mt-5 field submitbtn" title="Add Admin">
                    Add Admin
                </button>
                
            </form>
        </div>
        <!-- Success modal -->
        <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
    </div>
</template>
<script>
import DefaultModal from "@/components/DefaultModal.vue";
import { useVuelidate } from "@vuelidate/core";
import { required, helpers, email} from "@vuelidate/validators";
import UserManagementService from "@/api/services/UserManagementService";

export default {
    name: "AddAdmin",
    setup() {
        const v$ = useVuelidate(); 
        return { v$ };
    },
    data() {
        return {
            //Form Fields
            formData: {
                emailAddress: "",
                fullName: ""
            },
            //Modal
            title: "",
            message: "",
            buttonType: "",
            showAlert: false,
            userID: 0,
            submitFormData: {}
        }
    },
    components: {
        DefaultModal
    },
    validations() {
        return {
            formData: {
                emailAddress: { required: helpers.withMessage('Please provide a valid email', required), email: helpers.withMessage('Please provide a valid email', email) },
                fullName: { required: helpers.withMessage('Please provide a valid full name', required) }
            }
        }
    },
    created() {
        document.title = "Add Admin | Upskilling Engagement System";
    },
    methods: {
        async handleModalClosed(value){
            this.showAlert = value;

            if(!this.showAlert) {
                this.$router.push('/adminViewManagement');
            }
        },
        async addAdmin() {
            try {
                this.addAdminResponse = await UserManagementService.addAdmin(this.submitFormData);
            } catch (error) {
                console.error("Error fetching a new user ", error);

                this.title = "User Creation Failed";

                throw new Error("User Creation was unsuccessful");
            }
        },
        setSuccessAlert(action) {
            this.title = `${action} Success`;
            this.message = `${action} was successful`;
            this.buttonType = "success";
            this.showAlert = !this.showAlert;
        },
        async onSubmit() {
            this.v$.$touch();

            if (!this.v$.$invalid) {

                console.log('Form has no validation errors');

                try {

                    this.submitFormData["user_Name"] = this.formData.fullName

                    this.submitFormData["user_Email"] = this.formData.emailAddress

                    this.submitFormData ["role_Name"] = "Admin"

                    console.log(this.submitFormData)

                    await this.addAdmin();

                    this.setSuccessAlert("User Creation");

                } catch(error) {
                    const errorMsgParts = error.toString().split(":")
                    this.message = errorMsgParts[1];
                    this.buttonType = "danger"
                    this.showAlert = !this.showAlert;
                }
               
            } else {

                console.log('Form has validation errors');

            }
        },
        goToAdminViewManagement(){
            this.$router.push("/adminViewManagement");
        }
    }
}
</script>