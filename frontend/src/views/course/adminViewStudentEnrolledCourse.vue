<template>
  <div>
    <search-filter
      :search-api="searchStudentCourse"
      @search-complete="handlePageChange"
    />

    <div class="container col-12">
      <h5 class="pb-3">{{student_Name}}'s Enrolled Course</h5>
      <div v-if="registered_courses && registered_courses.length > 0" class="table-responsive">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'registered')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Startdate', 'registered')">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('run_Enddate', 'registered')">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
              <th scope="col">Course Details</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(registered_course, key) in displayedRegisteredCourses" :key="key">
              <td>
                <course-name-desc :name="registered_course.course_Name" :category="registered_course.coursecat_Name" :description="registered_course.course_Desc"></course-name-desc>
              </td>
              <td>
                <course-date-time :date="registered_course.run_Startdate" :time="registered_course.run_Starttime"></course-date-time>
              </td>
              <td>
                <course-date-time :date="registered_course.run_Enddate" :time="registered_course.run_Endtime"></course-date-time>
              </td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(registered_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
              
            </tr>
          </tbody>
        </table>
        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
        </div>
      </div>
      <div v-else-if="registered_courses=[]">
          <p>No enrolled course</p>
      </div>

    </div>

    <vue-awesome-paginate
      v-if="registered_courses.length/itemsPerPage > 0"
      v-model="localCurrentPageRegistered"
      :totalItems="registered_courses.length"
      :items-per-page="itemsPerPage"
      @page-change="handlePageChangeRegistered"
      class="justify-content-center pagination-container"
    />

    <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
      <div class="modal-dialog modal-lg"> 
        <modal-after-action :course="actionCourse" @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal" />
      </div>
    </div>
  </div>
</template>

<script>
// import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import courseDateTime from '@/components/course/courseDateTime.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/ProposalCourseRelatedSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";
import modalAfterAction from '@/components/course/modalAfterAction.vue';
import CommonService from '@/api/services/CommonService';
import ManagementService from "@/api/services/UserManagementService.js";

export default {
  components: {
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    SearchFilter,
    courseDateTime,
    modalAfterAction,
  },
  data() {
    return {
      registered_courses: [],
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageRegistered: 1,
      statusOptionsRegistered: ["Enrolled", "Pending", "Not Enrolled", "Dropped"],
      currentDate: new Date(),
      receivedMessage: '',
      actionCourse: {},
      user_ID: null,
      student_Name: ''
    }
  },
  async created() {
    const { user_ID } = this.$route.params;
    this.user_ID = user_ID

    let response = await ManagementService.getStudentName(this.user_ID);
    this.student_Name = response.data

    const registeredCourses = await CourseService.adminGetUserCourses(this.user_ID, null, null);
    this.registered_courses = registeredCourses.data;

    
    
  },
  methods: {
    openModal(course) {
      this.selectedCourse = course;
      this.showModal = true;
    },
    closeModal() {
      this.selectedCourse = null;
      this.showModal = false;
    },
    handleActionData(actionData) {
      this.receivedMessage = actionData.message;
      this.actionCourse = actionData.course
      const modalButtonElement = this.$el.querySelector('.invisible-btn')
      modalButtonElement.click();
    },
    
    handlePageChange(newPage) {
      this.localCurrentPageRegistered = newPage;
      this.$emit('page-change', newPage);
    },
    
    async handleSearchCompleteRegistered(searchResults) {
      this.registered_courses = searchResults;
    },

    async searchStudentCourse(user_ID, course_Name, coursecat_ID) {
      try {
        user_ID = this.user_ID

        let response = await CourseService.adminGetUserCourses(
          user_ID,
          course_Name,
          coursecat_ID,
        );
        this.registered_courses = response.data;
        return this.registered_courses;
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
        this.sortDirection = 'asc';
      }
      this.sortCourse(action)
    },
    getSortDirection(column) {
      if (this.sortColumn === column) {
        return this.sortDirection;
      }
    },
    async sortCourse() {
     
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.registered_courses)
        if (sort_response.code == 200) {
        this.registered_courses = sort_response.data
         }
    },
    isClosingDateValid(closingDate) {
        const regClosingDate = new Date(closingDate);
        return this.currentDate < regClosingDate;
    },
    
  },
  computed: {
    displayedRegisteredCourses() {
      const startIndex = (this.localCurrentPageRegistered - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.registered_courses.slice(startIndex, endIndex);
    },
    
  }
}
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>