<template>
  <div>
  <ul class="nav nav-pills justify-content-center mb-5">
    <li class="nav-item">
      <a class="nav-link" :class="{ 'active': activeTab === 'admin' }" @click="activeTab = 'admin'">All Admin</a>
    </li> 
    <li class="nav-item">
      <a class="nav-link" :class="{ 'active': activeTab === 'student' }" @click="activeTab = 'student'">All Student</a>
    </li>
    <li class="nav-item">
      <a class="nav-link" :class="{ 'active': activeTab === 'instructor' }" @click="activeTab = 'instructor'">All Instructor/Trainer</a>
    </li>
  </ul>

  <!-- All Admin -->
  <div class="tab-content ">
    <div class="tab-pane fade" :class="{ 'show active': activeTab === 'admin' }">
      <NameSearchFilter
      :search-api="searchAdminInfo"
      @search-complete="handleSearchAdmin" />

      <div class="container col-12 d-flex mb-3 w-100">
          <h5 class="col m-auto">All Admin Database</h5>
          <button class="btn btn-primary font-weight-bold text-nowrap" @click="goToAddAdmin">Add Admin</button>
      </div>

      <div class="container col-12">
        <div v-if="admin && admin.length > 0" class="table-responsive">
          <table class="table bg-white">
            <thead>
              <tr class="text-nowrap">
                <th scope="col">
                  <a href="" class="text-decoration-none text-dark" @click.prevent="sort('user_Name', 'admin')">Name <sort-icon :sortColumn="sortColumn === 'user_Name'" :sortDirection="getSortDirection('user_Name')"/></a>
                </th>
                <th scope="col">Email</th>
                <th scope="col">Action(s)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, key) in displayedAdmin" :key="key">
                <td class="user_name">
                  {{ user.user_Name }}
                </td>
                <td class="user_email">
                  {{ user.user_Email }}
                </td>

                <td v-if="user.user_ID !== user_ID">
                  <button class="btn btn-danger font-weight-bold text-nowrap" @click="removeAdmin(user.user_ID)">Remove</button>
                </td>
                <td v-else></td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else-if="admin=[]">
          <p>No records found</p>
        </div>
      </div>
      <vue-awesome-paginate v-if="admin.length/itemsPerPage > 0" v-model="localCurrentPageAdmin" :totalItems="admin.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeAdmin" class="justify-content-center pagination-container"/>
    </div>

    <!-- All Student  -->
    <div class="tab-pane fade" :class="{ 'show active': activeTab === 'student' }">
      <StudentSearchFilter
        :status-options="blacklistedOption"
        :search-api="searchStudentInfo"
        @search-complete="handleSearchStudent"
      />

      <div class="container col-12 d-flex mb-3 w-100">
          <h5 class="col m-auto">All Student Database</h5>
          <button v-show="showBlacklistButton" class="btn btn-danger me-3 font-weight-bold text-nowrap" @click="blacklist">Blacklist Student</button>
          <button v-show="showRemoveButton" class="btn btn-danger font-weight-bold text-nowrap" @click="removeFromBlacklist">Remove from Blacklist</button>
      </div>

      <div class="container col-12 table-responsive">
        <div v-if="student && student.length > 0">
          <table class="table bg-white">
            <thead>
              <tr class="text-nowrap">
                <th scope="col">
                </th>
                <th scope="col">
                  <a href="" class="text-decoration-none text-dark" @click.prevent="sort('user_Name', 'student')">Name <sort-icon :sortColumn="sortColumn === 'user_Name'" :sortDirection="getSortDirection('user_Name')"/></a>
                </th>
                <th scope="col">Email</th>
                <th scope="col">Blacklisted</th>
                <th scope="col">View Course Taken</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, key) in displayedStudent" :key="key">
                <td class="user_checkbox">
                  <!-- Bind checkbox to the selectedUserIDs array -->
                  <input type="checkbox" v-model="selectedUserIDs" :value="user.user_ID" />
                </td>
                <td class="user_name">
                  {{ user.user_Name }}
                </td>
                <td class="user_email">
                  {{ user.user_Email }}
                </td>
                <td class="is_blacklisted">
                  <span v-if="user.is_blacklisted === true" class="text-danger">Blacklisted</span>
                  <span v-else>Not Blacklisted</span>
                </td>
                <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis" @click="viewCourses(user.user_ID)">View Course Taken</a></td>
              </tr> 
            </tbody>
          </table>
        </div>
        <div v-else-if="student=[]">
          <p>No records found</p>
        </div>
      </div>
      <vue-awesome-paginate v-if="student.length/itemsPerPage > 0" v-model="localCurrentPageStudent" :totalItems="student.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeStudents" class="justify-content-center pagination-container"/>
    </div>

    <!-- All Instructor / Trainer -->
    <div class="tab-pane fade" :class="{ 'show active': activeTab === 'instructor' }">
        <search-filter
            :status-options="statusOptions"
            :search-api="getAllInstructorsAndTrainers"
            @search-complete="handleSearchComplete" />

        <div class="container col-12 table-responsive">
            <h5 class="pb-3">All Instructor/Trainer Database</h5>
            <div v-if="instructors_trainers && instructors_trainers.length > 0">
                <table class="table bg-white">
                <thead>
                    <tr class="text-nowrap">
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('user_Name', 'instructor')">Name <sort-icon :sortColumn="sortColumn === 'user_Name'" :sortDirection="getSortDirection('user_Name')"/></a>
                    </th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('role_Name', 'instructor')">Role <sort-icon :sortColumn="sortColumn === 'role_Name'" :sortDirection="getSortDirection('role_Name')"/></a>
                    </th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('organisation_Name', 'instructor')">Organization <sort-icon :sortColumn="sortColumn === 'organisation_Name'" :sortDirection="getSortDirection('organisation_Name')"/></a>
                    </th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('average_rating', 'instructor')">Ratings <sort-icon :sortColumn="sortColumn === 'average_rating'" :sortDirection="getSortDirection('average_rating')"/></a>
                    </th>
                    <th scope="col">Feedback Analysis</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(instructor_trainer, key) in displayedInstructorsTrainers" :key="key">
                    <td class="user_name">
                        {{ instructor_trainer.user_Name }}
                    </td>
                    <td class="user_role">
                        {{ instructor_trainer.role_Name }}
                    </td>
                    <td class="orgnanization">
                        {{ instructor_trainer.organisation_Name }}
                    </td>
                    <td class="ratings">
                        {{ instructor_trainer.average_rating }} / 5
                    </td>
                    <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis">View Feedback Analysis</a></td>
                    </tr>
                </tbody>
                </table>
            </div>
            <div v-else-if="instructors_trainers=[]">
                <p>No records found</p>
            </div>
        </div>
        <vue-awesome-paginate v-if="instructors_trainers.length/itemsPerPage > 0" v-model="localCurrentPageInstructorsTrainers" :totalItems="instructors_trainers.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeInstructorsTrainers" class="justify-content-center pagination-container"/>
    </div>

    <div class="modal fade" id="course_details_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" />
      </div>
    </div>

    <DefaultModal :visible="showModal" :message="modalMessage" :title="modalTitle" :variant="modalVariant" @modal-closed="handleModalClosed"/>
  </div>
</div>
</template>

<script>
import sortIcon from '@/components/common/sort-icon.vue';
import modalCourseContent from '@/components/course/modalCourseContent.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/InstructorRelatedSearchFilter.vue";
import StudentSearchFilter from "@/components/search/StudentInfoSearchFilter.vue";
import NameSearchFilter from "@/components/search/NameSearchFilter.vue";
import ManagementService from "@/api/services/UserManagementService.js";
import CommonService from "@/api/services/CommonService.js"
import UserService from "@/api/services/UserService.js";
import DefaultModal from "@/components/DefaultModal.vue";

export default {
  components: {
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    DefaultModal,
    SearchFilter,
    StudentSearchFilter,
    NameSearchFilter
  },
  data() {
    return {
      // Admin
      admin: [],
      localCurrentPageAdmin: 1,
      student: [],
      localCurrentPageStudent: 1,
      blacklistedOption: ['Blacklisted', 'Not Blacklisted'],
      search_name: null,
      search_blacklist: null, 
      activeTab: 'admin',
      receivedMessage: '',
      actionCourse: {},
      search_course_name: null,
      search_course_category: null,
      instructors_trainers: [],
      sortColumn: '',
      sortDirection: 'asc',
      itemsPerPage: 10,
      localCurrentPageInstructorsTrainers: 1,
      statusOptions: ["Instructor", "Trainer"],
      selectAllStudents: false,
      selectedUserIDs: [],
      showModal: false,
      modalMessage: "",
      modalTitle: "",
      modalVariant: "secondary",
      userID: null,
    }
  },
  methods: {
    handlePageChangeAdmin(newPage) {
      this.localCurrentPageAdmin = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeStudents(newPage) {
      this.localCurrentPageStudent = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeInstructorsTrainers(newPage) {
      this.localCurrentPageInstructorsTrainers = newPage;
      this.$emit('page-change', newPage);
    },
    async handleSearchComplete(searchResults) {
      this.instructors_trainers = searchResults;
    },
    async handleSearchStudent(searchResults) {
      this.student = searchResults;
    },
    async handleSearchAdmin(searchResults) {
      this.admin = searchResults;
    },
    async searchAdminInfo(user_Name) {
    
      try {
        let response = await ManagementService.getAllAdmin(
          user_Name,
        );
        this.admin = response.data;
        return this.admin;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    async searchStudentInfo(user_Name, blacklisted) {
      console.log(user_Name)
      try {
        if (blacklisted === "Blacklisted") {
          this.search_blacklist = true;
        } else if (blacklisted === "Not Blacklisted") {
          this.search_blacklist = false;
        }

        this.search_name = user_Name;
        let response = await ManagementService.getAllStudent(
          user_Name,
          this.search_blacklist
        );
        this.student = response.data;
        return this.student;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    async getAllInstructorsAndTrainers(user_Name, role_Name, organizationName) {
      try {
        let response = await ManagementService.getAllInstructorsAndTrainers(
          user_Name,
          role_Name,
          organizationName
        );
        this.instructors_trainers = response.data;
        return this.instructors_trainers;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    sort(column, action) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = column === 'average_rating' ? 'desc' : 'asc';
      }
      this.sortCourse(action);
    },
    getSortDirection(column) {
      if (this.sortColumn === column) {
        return this.sortDirection;
      }
    },
    async sortCourse(action) {
      if (action == 'admin') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.admin)
          if (sort_response.code == 200) {
          this.admin = sort_response.data
          }
      }
      if (action == 'student') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.student)
          if (sort_response.code == 200) {
          this.student = sort_response.data
          }
      }
      if (action == 'instructor') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.instructors_trainers)
        if (sort_response.code == 200) {
          this.instructors_trainers = sort_response.data
        }
      }

    },
    async loadData() {
      try {
        let admin_response = await ManagementService.getAllAdmin(null)
        this.admin = admin_response.data

        let student_response = await ManagementService.getAllStudent(null, null)
        this.student = student_response.data

        let response = await ManagementService.getAllInstructorsAndTrainers(null, null, null)
        this.instructors_trainers = response.data
        
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    },
    goToAddAdmin() {
      this.$router.push({name: 'adminAddAdmin'})
    },
    viewCourses(user_ID) {
      this.$router.push({ name: 'adminViewStudentEnrolledCourse', params: { user_ID } });
    },
    async handleModalClosed(){
      this.loadData()
      this.selectedUserIDs = []
    },
    async blacklist() {
      this.modalTitle = "Blacklist Student"

      if (this.selectedUserIDs.length === 0) {
        this.modalMessage = "You did not select any student to blacklist."
        this.showModal = true;
      }

      let response = await ManagementService.blacklistStudent(this.selectedUserIDs)
      this.modalMessage = response.message
      this.showModal = true;
    },
    async removeFromBlacklist() {
      this.modalTitle = "Remove Student from Blacklist"
      if (this.selectedUserIDs.length === 0) {
        this.modalMessage = "You did not select any student to remove from blacklist."
        this.showModal = true;
      }

      let response = await ManagementService.removeFromBlacklist(this.selectedUserIDs)
      this.modalMessage = response.message
      this.showModal = true;
    },
    async removeAdmin(user_ID) {
      this.modalTitle = "Remove Admin"
      console.log(user_ID)
      let response = await ManagementService.removeAdmin(user_ID)
      this.modalMessage = response.message
      this.showModal = true;
    },
  },
  computed: {
    displayedAdmin() {
      const startIndex = (this.localCurrentPageAdmin - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.admin.slice(startIndex, endIndex);
    },

    displayedStudent() {
      const startIndex = (this.localCurrentPageStudent - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.student.slice(startIndex, endIndex);
    },

    displayedInstructorsTrainers() {
      const startIndex = (this.localCurrentPageInstructorsTrainers - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.instructors_trainers.slice(startIndex, endIndex);
    },
    showBlacklistButton() {
      return this.search_blacklist === false || this.search_blacklist === null;
    },
    showRemoveButton() {
      return this.search_blacklist === true || this.search_blacklist === null;
    },
  },
  async created() {
    const user_ID = await UserService.getUserID();
    this.user_ID = user_ID;
    const role = await UserService.getUserRole(user_ID);
    if (role != 'Admin') {
      this.$router.push({ name: 'studentViewProfile' }); 
    } else {
      try {
        let admin_response = await ManagementService.getAllAdmin(null)
        this.admin = admin_response.data

        let student_response = await ManagementService.getAllStudent(null, null)
        this.student = student_response.data

        let response = await ManagementService.getAllInstructorsAndTrainers(null, null, null)
        this.instructors_trainers = response.data
      } catch (error) {
        console.error("Error fetching course details:", error);
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