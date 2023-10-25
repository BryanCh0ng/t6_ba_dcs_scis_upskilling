<template>
  <div>
    <ul class="nav nav-pills justify-content-center pt-4">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'course_reg' }" @click="activeTab = 'course_reg'">Courses Available to Register</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'course_vote' }" @click="activeTab = 'course_vote'">Courses Available to Vote</a>
      </li>
    </ul>
    <div class="tab-content">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'course_reg' }">
        <search-filter :search-api="searchUnregisteredActiveInfo" @search-complete="handleSearchCompleteRun"/>

        <div class="container col-12">
          <h5 class="pb-3">All Courses Available to Register</h5>
          <div v-if="run_courses && run_courses.length > 0" class="table-responsive">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Name', 'run')">Course Name / Description
                      <sort-icon :sortColumn="sortColumn === 'run_Name'" :sortDirection="getSortDirection('run_Name')"/>
                    </a>
                  </th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'run')" >Course Start Date
                      <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/>
                    </a>
                  </th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'run')" >Course End Date
                      <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/>
                    </a>
                  </th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'run')">Closing Date
                      <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/>
                    </a>
                  </th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(course, key) in displayedRunCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="course.run_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
                  </td>
                  <td class="start_date">
                    <course-date-time :date="course.run_Startdate" :time="course.run_Starttime"></course-date-time>
                  </td>
                  <td class="end_date">
                    <course-date-time :date="course.run_Enddate" :time="course.run_Endtime" ></course-date-time>
                  </td>
                  <td class="closing_date">
                    <course-date-time :date="course.reg_Enddate" :time="course.reg_Endtime"></course-date-time>
                  </td>
                  <td>
                    <a class="text-nowrap text-dark text-decoration-underline view-course-details" @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a>
                  </td>
                  <td>
                    <course-action @action-and-message-updated="handleActionData" :status="course.course_Status" :course="course"></course-action>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="(run_courses = [])">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="run_courses.length / itemsPerPage > 0" v-model="localCurrentPageRunCourse" :totalItems="run_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
      </div>

      <!-- Courses available to vote -->
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'course_vote' }">
        <search-filter :search-api="searchUnvotedActiveInfo" @search-complete="handleSearchCompleteVote"/>

        <div class="container col-12 table-responsive">
          <h5 class="pb-3">Courses Available to Vote</h5>
          <div v-if="vote_courses && vote_courses.length > 0">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'vote')">Course Name / Description
                      <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a>
                  </th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(course, key) in displayVoteCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="course.course_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
                  </td>
                  <td>
                    <a class="text-nowrap text-dark text-decoration-underline view-course-details" @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a>
                  </td>
                  <td>
                    <course-action @action-and-message-updated="handleActionData" status="Vote" :course="course"></course-action>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="(vote_courses = [])">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="vote_courses.length / itemsPerPage > 0" v-model="localCurrentPageVoteCourse" :totalItems="vote_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
      </div>
      <div class="modal fade" id="course_details_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal"/>
        </div>
      </div>

      <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
        <div class="modal-dialog modal-lg">
          <modal-after-action :course="actionCourse" @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import courseAction from "@/components/course/courseAction.vue";
import sortIcon from "@/components/common/sort-icon.vue";
import modalCourseContent from "@/components/course/modalCourseContent.vue";
import courseNameDesc from "@/components/course/courseNameDesc.vue";
import courseDateTime from "@/components/course/courseDateTime.vue";
import { VueAwesomePaginate } from "vue-awesome-paginate";
import SearchFilter from "@/components/search/StudentCourseSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";
import UserService from "@/api/services/UserService.js";
import modalAfterAction from "@/components/course/modalAfterAction.vue";
import CommonService from "@/api/services/CommonService.js";

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    courseNameDesc,
    VueAwesomePaginate,
    courseDateTime,
    SearchFilter,
    modalAfterAction,
  },
  data() {
    return {
      user_ID: null,
      run_courses: [],
      vote_courses: [],
      sortColumn: "",
      sortDirection: "asc",
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageRunCourse: 1,
      localCurrentPageVoteCourse: 1,
      activeTab: "course_reg",
      receivedMessage: "",
      actionCourse: {},
      search_course_name: null,
      search_course_category: null,
    };
  },
  computed: {
    displayedRunCourses() {
      const startIndex = (this.localCurrentPageRunCourse - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.run_courses.slice(startIndex, endIndex);
    },
    displayVoteCourses() {
      const startIndex = (this.localCurrentPageVoteCourse - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.vote_courses.slice(startIndex, endIndex);
    },
  },
  methods: {
    async get_user_id() {
      try {
        const user_ID = await UserService.getUserID();
        this.user_ID = user_ID;
      } catch (error) {
        this.message = error.message;
        this.user_ID = null;
      }
    },
    openModal(course) {
      this.selectedCourse = course;
      this.showModal = true;
    },
    closeModal() {
      this.selectedCourse = null;
      this.showModal = false;
    },
    handlePageChange(newPage) {
      this.localCurrentPage = newPage;
      this.$emit("page-change", newPage);
    },
    async handleSearchCompleteRun(searchResults) {
      console.log(searchResults);
      this.run_courses = searchResults;
    },
    async handleSearchCompleteVote(searchResults) {
      this.vote_courses = searchResults;
    },
    async searchUnregisteredActiveInfo(user_ID, course_Name, coursecat_ID) {
      this.search_course_name = course_Name;
      this.search_course_category = coursecat_ID;
      try {
        // console.log(course_Name)
        let response = await CourseService.searchUnregisteredActiveInfo(
          user_ID,
          course_Name,
          coursecat_ID
        );
        this.run_courses = response.data;
        return this.run_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    async searchUnvotedActiveInfo(user_ID, course_Name, coursecat_ID) {
      this.search_course_name = course_Name;
      this.search_course_category = coursecat_ID;
      try {
        // console.log(coursecat_ID)
        let response = await CourseService.searchUnvotedActiveInfo(
          user_ID,
          course_Name,
          coursecat_ID
        );
        this.vote_courses = response.data;
        return this.vote_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    handleActionData(actionData) {
      this.receivedMessage = actionData.message;
      this.actionCourse = actionData.course;
      const modalButtonElement = this.$el.querySelector(".invisible-btn");
      modalButtonElement.click();
    },
    async loadData() {
      try {
        await this.getUserID();
        let run_response = await CourseService.searchUnregisteredActiveInfo(
          this.user_ID,
          this.search_course_name,
          this.search_course_category
        );
        this.run_courses = run_response.data;

        let vote_response = await CourseService.searchUnvotedActiveInfo(
          this.user_ID,
          this.search_course_name,
          this.search_course_category
        );
        this.vote_courses = vote_response.data;
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    },
    modalAfterActionClose() {
      this.loadData();
    },
    sort(column, action) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
      } else {
        this.sortColumn = column;
        this.sortDirection = "asc";
      }
      this.sortCourse(action);
    },
    getSortDirection(column) {
      if (this.sortColumn === column) {
        return this.sortDirection;
      }
    },
    async sortCourse(action) {
      if (action == "run") {
        let sort_response = await CommonService.sortRecords(
          this.sortColumn,
          this.sortDirection,
          this.run_courses
        );
        if (sort_response.code == 200) {
          this.run_courses = sort_response.data;
        }
      }
      if (action == "vote") {
        let sort_response = await CommonService.sortRecords(
          this.sortColumn,
          this.sortDirection,
          this.vote_courses
        );
        if (sort_response.code == 200) {
          this.vote_courses = sort_response.data;
        }
      }
    },
    async getUserID() {
      try {
        const user_ID = await UserService.getUserID();
        this.user_ID = user_ID;
      } catch (error) {
        console.error("Error fetching user ID:", error);
        this.user_ID = null;
      }
    },
  },
  async created() {
    const user_ID = await UserService.getUserID();
    this.user_ID = user_ID;
    const role = await UserService.getUserRole(user_ID);
    if (role == "Admin") {
      this.$router.push({ name: "adminViewCourse" });
    } else if (role == "Instructor" || role == "Trainer") {
      this.$router.push({ name: "instructorTrainerViewVotingCampaign" });
    } else {
      try {
        this.loadData();
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    }
  },
  mounted() {
    const buttonElement = document.createElement("button");
    buttonElement.className = "btn btn-primary d-none invisible-btn";
    buttonElement.setAttribute("data-bs-toggle", "modal");
    buttonElement.setAttribute("data-bs-target", "#after_action_modal");
    this.$el.appendChild(buttonElement);
    const modalElement = this.$refs.afterActionModal;
    modalElement.addEventListener(
      "hidden.bs.modal",
      this.modalAfterActionClose
    );
  },
  beforeUnmount() {
    const modalElement = this.$refs.afterActionModal;
    modalElement.removeEventListener(
      "hidden.bs.modal",
      this.modalAfterActionClose
    );
  },
};
</script>

<style>
@import "../../assets/css/course.css";
@import "../../assets/css/paginate.css";
</style>
