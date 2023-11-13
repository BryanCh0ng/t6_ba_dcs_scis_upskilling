<template>
  <div>
    <StudentSearchFilter :status-options="statusOption" :search-api="searchStudentInfo"
      @search-complete="handleSearchStudent" />

    <div class="container col-12 d-flex mb-3 w-100">
      <h5 class="col m-auto">All Registration Status for '{{ this.runCourseName }}'</h5>
      <div v-if="shouldShowActionButtons" class="dropdown">
        <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
          Action
        </button>
        <ul class="dropdown-menu">
          <li v-if="status === null || status === 'Pending'"><a class="dropdown-item" @click="enrolStudent">Enroll Student</a></li>
          <li v-if="status === null || status === 'Enrolled'"><a class="dropdown-item" @click="dropStudent">Drop Student</a></li>
        </ul>
      </div>
    </div>

    <div class="container col-12">
      <div class="table-responsive" v-if="student && student.length > 0">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <input type="checkbox" v-if="hasActionableRecords" v-model="selectAllStudents"
                  @change="selectAllStudentsChanged" />
              </th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('user_Name', 'student')">Name
                  <sort-icon :sortColumn="sortColumn === 'user_Name'"
                    :sortDirection="getSortDirection('user_Name')" /></a>
              </th>
              <th scope="col">Email</th>
              <th scope="col">Blacklist Status</th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark"
                  @click.prevent="sort('reg_Status', 'student')">Registration Status
                  <sort-icon :sortColumn="sortColumn === 'reg_Status'"
                    :sortDirection="getSortDirection('reg_Status')" /></a>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in displayedStudent" :key="user.reg_ID">
              <td class="user_checkbox">
                <!-- Bind checkbox to the selectedUserIDs array -->
                <input v-if="user.reg_Status === 'Pending' || user.reg_Status === 'Enrolled'" type="checkbox"
                  :value="user.reg_ID" :checked="selectedRegIDs.includes(user.reg_ID)" @change="selectUser(user)" />
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

    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType"
      @modal-closed="handleModalClosed" />
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
      statusOption: ['Pending', 'Enrolled', 'Not Enrolled', 'Dropped'],
      user_ID: null,
      runCourseID: null,
      localCurrentPageStudent: 1,
      itemsPerPage: 10,
      student: [],
      name: "",
      status: null,
      runCourseName: "",
      errorMsg: [],
      title: "",
      message: "",
      buttonType: "",
      showAlert: false,
      selectAllStudents: false,
      selectedRegIDs: [],
      sortColumn: '',
      sortDirection: 'asc'
    }
  },
  async created() {
    const user_ID = await UserService.getUserID();
    this.user_ID = user_ID;
    const role = await UserService.getUserRole(user_ID);

    if (role == 'Student') {
      this.$router.push({ name: 'studentViewCourse' });
    } else if (role == 'Instructor' || role == 'Trainer') {
      this.$router.push({ name: 'instructorTrainerViewLesson' }); //Need to change
    } else if (role == 'Admin') {
      document.title = "Run Course Registration | Upskilling Engagement System"; //Need to change 
      this.runCourseID = this.$route.params.id;
      await this.loadData();
    }
  },
  computed: {  
    shouldShowActionButtons() {
      return this.status === null ||
             this.status === 'Pending' ||
             this.status === 'Enrolled';
    },
    displayedStudent() {
      const startIndex = (this.localCurrentPageStudent - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.student.slice(startIndex, endIndex);
    },
    hasActionableRecords() {
      return this.student.some(user => user.reg_Status === 'Pending' || user.reg_Status === 'Enrolled');
    }
  },
  methods: {
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
    handleModalClosed(value) {
      this.showAlert = value;

      if (!this.showAlert && this.buttonType === "success") {
        window.location.reload();
      }

      //Clear the select all checkbox
      this.selectAllStudents = false;

      //Clear selected checkbox or checkboxes
      this.selectedRegIDs = [];
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
            .filter(user => user.reg_Status === 'Pending' || user.reg_Status === "Enrolled")
            .map(user => user.reg_ID);
        } else {
          // Deselect all users
          this.selectedRegIDs = [];
        }
      }, 0);
    },
    selectUser(user) {
      const regID = user.reg_ID;

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
    async enrolStudent() {
      try {
        this.selectedRegIDs = JSON.stringify(this.selectedRegIDs)
        let response = await RegistrationService.enrollStudent(this.selectedRegIDs)

        if (response.data.code === 200) {
          this.title = "Run Course Enrollement Successful";
          this.message = response.data.message;
          this.buttonType = "success";
        } else if (response.data.code === 400 || response.data.code === 404) {
          this.title = "Run Course Enrollement Failed";
          this.message = response.data.message;
          this.buttonType = "danger";
        } else if (response.data.code === 500) {
          this.title = "Run Course Enrollement Failed";
          this.message = response.data.message.split(":")[0] + ": Something went wrong.";
          this.buttonType = "danger";
          console.log(response.data.message);
        }

        this.showAlert = !this.showAlert;

      } catch (error) {
        console.error("Error enrolling student(s): ", error);
      }
    },
    async dropStudent() {
      try {
        this.selectedRegIDs = JSON.stringify(this.selectedRegIDs)
        let response = await RegistrationService.dropStudent(this.selectedRegIDs)

        if (response.data.code === 200) {
          this.title = "Dropped Enrolled Student(s) Successfully";
          this.message = response.data.message
          this.buttonType = "success";
        } else if (response.data.code === 400 || response.data.code === 404) {
          this.title = "Dropped Enrolled Student(s) Failed";
          this.message = response.data.message
          this.buttonType = "danger";
        } else if (response.data.code === 500) {
          this.title = "Dropped Enrolled Student(s) Failed";
          this.message = response.data.message.split(":")[0] + ": Something went wrong.";
          this.buttonType = "danger";
          console.log(response.data.message);
        }

        this.showAlert = !this.showAlert;

      } catch (error) {
        console.error("Error enrolling student(s): ", error);
      }
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