<template>
  <div>
    <StudentSearchFilter :status-options="statusOption" :search-api="searchStudentInfo"
      @search-complete="handleSearchStudent" />

    <div class="container col-12 d-flex mb-3 w-100">
      <h5 class="col m-auto">All Registration Status for '{{this.runCourseName}}'</h5>
      <button class="btn btn-primary font-weight-bold text-nowrap"
        @click="enrolStudent">Enrol Student</button>
    </div>

    <div class="container col-12 table-responsive">
      <div v-if="student && student.length > 0">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <input type="checkbox" v-if="hasPendingRecords" v-model="selectAllStudents" @change="selectAllStudentsChanged" />
              </th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('user_Name', 'student')">Name
                  <sort-icon :sortColumn="sortColumn === 'user_Name'"
                    :sortDirection="getSortDirection('user_Name')" /></a>
              </th>
              <th scope="col">Email</th>
              <th scope="col">Blacklist Status</th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Status', 'student')" >Registration Status 
                  <sort-icon :sortColumn="sortColumn === 'reg_Status'" 
                  :sortDirection="getSortDirection('reg_Status')"/></a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, key) in displayedStudent" :key="key">
              <td class="user_checkbox">
                <!-- Bind checkbox to the selectedUserIDs array -->
                <input v-if="user.reg_Status === 'Pending'" type="checkbox" :value="user.reg_ID" :checked="selectedRegIDs.includes(user.reg_ID)" @change="selectUser(key)" />
              </td>
              <td class="user_name">
                {{ user.user_Name }}
              </td>
              <td class="user_email">
                {{ user.user_Email }}
              </td>
              <td class="blacklist_status">
                  <span v-if="user.blacklist_Status === 'Blacklisted'" class="text-danger">Blacklisted</span>
                  <span v-else>Not Blacklisted</span>
              </td>
              <td class="reg_status">
                {{ user.reg_Status }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="student = []">
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-if="student.length / itemsPerPage > 0" v-model="localCurrentPageStudent"
      :totalItems="student.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeStudents"
      class="justify-content-center pagination-container" />

    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
  </div>
</template>

<script>
import UserService from "@/api/services/UserService.js";
import RunCourseService from "@/api/services/runCourseService.js";
import RegistrationService from "@/api/services/RegistrationService.js";
import StudentSearchFilter from "@/components/search/StudentInfoSearchFilter.vue";
import sortIcon from '@/components/common/sort-icon.vue';
import CommonService from "@/api/services/CommonService.js"
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import DefaultModal from '@/components/DefaultModal.vue';

export default {
  components: {
    StudentSearchFilter,
    sortIcon,
    VueAwesomePaginate,
    DefaultModal
  },
  data() {
    return {
      user_ID: null,
      runCourseID: null,
      statusOption: ['Pending', 'Enrolled', 'Not Enrolled', 'Dropped'],
      runCourseName: "",
      errorMsg: [],
      student: [],
      //Modal 
      title: "",
      message: "",
      buttonType: "",
      showAlert: false,
      name: "",
      status: "", 
      sortColumn: '',
      sortDirection: 'asc',
      localCurrentPageStudent: 1,
      itemsPerPage: 10,
      selectAllStudents: false,
      selectedRegIDs: [],
      dataToUpdate: {},
      regID: null
    }
  },
  methods: {
    async fetchRunCourseName() {
      try {
        let response = await RunCourseService.getRunCourseById(this.runCourseID)
        this.runCourseName = response.run_Name;
      } catch (error) {
        console.error("Error fetching run course name: ", error)
        this.errorMsg.push("Error fetching run course name")
      }
    },
    async fetchRegistrationRecords() {
      try {
        let student_response = await RegistrationService.getRegistrationByRunCourseID(this.runCourseID, null, null)
        this.student = student_response.data
      } catch (error) {
        console.error("Error fetching registration records:", error);
        this.errorMsg.push("Error fetching registration records")
      }
    },
    async loadData() {
      await this.fetchRunCourseName();
      await this.fetchRegistrationRecords();

      if (this.errorMsg.length > 0) {
        this.title = "Data Retrieval Error";
        this.message = "There is a problem retrieving the registration data";
        this.buttonType = "danger";
        this.showAlert = !this.showAlert;
      }
    },
    async searchStudentInfo(user_Name, reg_Status) {
      try {
        this.name = user_Name
        this.status = reg_Status
        let response = await RegistrationService.getRegistrationByRunCourseID(this.runCourseID, this.name, this.status)
        this.student = response.data;
        return this.student;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    async handleSearchStudent(searchResults) {
      this.student = searchResults;
    },
    sort(column, action) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
      this.sortCourse(action);
    },
    getSortDirection(column) {
      if (this.sortColumn === column) {
        return this.sortDirection;
      }
    },
    async sortCourse(action) {
      if (action == 'student') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.student)
          if (sort_response.code == 200) {
            this.student = sort_response.data
          }
      }
    },
    selectAllStudentsChanged() {
      setTimeout(() => {
        if (this.selectAllStudents) {
          // Select all users
          this.selectedRegIDs = this.student
            .filter(user => user.reg_Status === 'Pending')
            .map(user => user.reg_ID);
        } else {
          // Deselect all users
          this.selectedRegIDs = [];
        }
      }, 0);
    },
    selectUser(key){
      const regID = this.student[key].reg_ID;

      if (this.selectedRegIDs.includes(regID)) {
      // User is already selected, so unselect them
        const index = this.selectedRegIDs.indexOf(regID);
        if (index !== -1) {
          this.selectedRegIDs.splice(index, 1);
        }
      } else {
        // User is not selected, so select them
        this.selectedRegIDs.push(regID);
      }
    },
    async enrolStudent(){
      const selectedData = [];
      for (let i = 0; i < this.selectedRegIDs.length; i++) {
          selectedData.push(this.selectedRegIDs[i]);
      }
      
      this.dataToUpdate["reg_Status"] = "Enrolled";

      for(let j = 0; j < selectedData.length; j++){
        try {
          let response = await RegistrationService.updateRegistration(selectedData[j], this.dataToUpdate)
          console.log(response);
        } catch (error) {
          console.error("Error updating the registration: ", error);
        }
      }

      this.title = "Enrollement Successful";
      this.message = "The student(s) have been successfully enrolled";
      this.buttonType = "success";
      this.showAlert = !this.showAlert;

    },
    handleModalClosed(value) {
      this.showAlert = value;

      if (!this.showAlert && this.buttonType === "success") {
        this.loadData();
      }
    }, 
  },
  computed: {
    displayedStudent() {
      const startIndex = (this.localCurrentPageStudent - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.student.slice(startIndex, endIndex);
    },
    hasPendingRecords() {
      return this.student.some(user => user.reg_Status === 'Pending');
    }
  },
  async created() {
    const user_ID = await UserService.getUserID();
    this.user_ID = user_ID;
    const role = await UserService.getUserRole(user_ID);

    if (role == 'Student') {
      this.$router.push({ name: 'studentViewProfile' });
    } else if (role == 'Instructor' || role == 'Trainer') {
      this.$router.push({ name: 'instructorTrainerViewProfile' });
    } else if (role == 'Admin') {
        //document.title = "Create a Run Course";
        this.runCourseID = this.$route.params.id;
        this.loadData();
    }
  }
};
</script>

<style>
@import '../../assets/css/course.css';
@import '../../assets/css/paginate.css';

.user_checkbox input[type="checkbox"] {
  transform: scale(1.2);
}
</style>