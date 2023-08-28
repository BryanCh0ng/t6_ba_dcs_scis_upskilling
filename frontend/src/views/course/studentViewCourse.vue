<template>
  <div>
  <ul class="nav nav-pills justify-content-center">
    <li class="nav-item">
      <a class="nav-link" :class="{ 'active': activeTab === 'course_reg' }" @click="activeTab = 'course_reg'">Courses Available to Register</a>
    </li> 
    <li class="nav-item">
      <a class="nav-link" :class="{ 'active': activeTab === 'course_vote' }" @click="activeTab = 'course_vote'">Courses Available to Vote</a>
    </li>
  </ul>
  <div class="tab-content ">
    <div class="tab-pane fade" :class="{ 'show active': activeTab === 'course_reg' }">
      <search-filter
      :search-api="searchUnregisteredActiveInfo"
      @search-complete="handleSearchCompleteRun" />
  
      <div class="container col-12 table-responsive">
        <h5 class="pb-3">All Courses Available to Register</h5>
        <div v-if="run_courses && run_courses.length > 0">
          <table class="table">
            <thead>
              <tr class="text-nowrap">
                <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon ::sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Course Start Date <sort-icon :sortColumn="sortColumn === 'start_date'" :sortDirection="sortDirection"/></a></th>
                <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Course End Date <sort-icon :sortColumn="sortColumn === 'end_date'" :sortDirection="sortDirection"/></a></th>
                <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
                <th scope="col">Course Details</th>
                <th scope="col">Action(s)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(course, key) in displayedRunCourses" :key="key">
                <td class="name">
                  <course-name-desc :name="course.course_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
                </td>
                <td class="start_date">
                  <course-date-time :date="course.run_Startdate" :time="course.run_Starttime"></course-date-time>
                </td>
                <td class="end_date">
                  <course-date-time :date="course.run_Enddate" :time="course.run_Endtime"></course-date-time>
                </td>
                <td class="closing_date">
                  <course-date-time :date="course.reg_Enddate" :time="course.reg_Endtime"></course-date-time>
                </td>
                <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                <td><course-action :status="course.course_Status" :id="course.rcourse_ID"></course-action></td>
              </tr>
            </tbody>
          </table>
          <div class="modal fade" id="course_details_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
              <modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" />
            </div>
          </div>
        </div>
        <div v-else-if="run_courses=[]">
          <p>No records found</p>
        </div>
      </div>
      <vue-awesome-paginate v-if="run_courses.length/itemsPerPage > 0" v-model="localCurrentPageRunCourse" :totalItems="run_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
    </div>
    <div class="tab-pane fade" :class="{ 'show active': activeTab === 'course_vote' }">
      <search-filter
      :search-api="searchUnvotedActiveInfo"
      @search-complete="handleSearchCompleteVote" />
  
      <div class="container col-12 table-responsive">
        <h5 class="pb-3">Courses Available to Vote</h5>
        <div v-if="vote_courses && vote_courses.length > 0">
          <table class="table">
            <thead>
              <tr class="text-nowrap">
                <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon ::sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                <th scope="col">Course Details</th>
                <th scope="col">Action(s)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(course, key) in displayVoteCourses" :key="key">
                <td class="name">
                  <course-name-desc :name="course.course_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
                </td>
                <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                <td><course-action :status="course.vote_Status" :id="course.course_ID"></course-action></td>
              </tr>
            </tbody>
          </table>
          <div class="modal fade" id="course_details_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
              <modal-course-content v-if="selectedCourse" :status="selectedCourse.course_Status" :course="selectedCourse" @close-modal="closeModal" />
            </div>
          </div>
        </div>
        <div v-else-if="vote_courses=[]">
          <p>No records found</p>
        </div>
      </div>
      <vue-awesome-paginate v-if="vote_courses.length/itemsPerPage > 0" v-model="localCurrentPageVoteCourse" :totalItems="vote_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
    </div>
    
  </div>
</div>
</template>

<script>
import courseAction from '@/components/course/courseAction.vue';
import sortIcon from '@/components/common/sort-icon.vue';
import modalCourseContent from '@/components/course/modalCourseContent.vue';
import courseNameDesc from '@/components/course/courseNameDesc.vue';
import courseDateTime from '@/components/course/courseDateTime.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/StudentCourseSearchFilter.vue";
import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'
import CourseService from "@/api/services/CourseService.js";

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    courseNameDesc,
    VueAwesomePaginate,
    courseDateTime,
    SearchFilter
  },
  data() {
    return {
      run_courses: [],
      vote_courses: [],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageRunCourse: 1,
      localCurrentPageVoteCourse: 1,
      activeTab: 'course_reg'
    }
  },
  computed: {
    displayedRunCourses() {
      const startIndex = (this.localCurrentPageRunCourse - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.run_courses.slice(startIndex, endIndex);
    },
    displayVoteCourses() {
      const startIndex = (this.localCurrentPageProposed - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.vote_courses.slice(startIndex, endIndex);
    }
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
    handlePageChange(newPage) {
      this.localCurrentPage = newPage;
      this.$emit('page-change', newPage);
    },
    async handleSearchCompleteRun(searchResults) {
      console.log(searchResults)
      this.run_courses = searchResults;
    },
    async handleSearchCompleteVote(searchResults) {
      this.vote_courses = searchResults;
    },
    async searchUnregisteredActiveInfo(user_ID, course_Name, coursecat_ID) {
      try {
        console.log(course_Name)
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
      try {
        console.log(coursecat_ID)
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
    }
  },
  async created() {
    try {
      let run_response = await CourseService.searchUnregisteredActiveInfo(null, null, null)
      console.log(run_response)
      this.run_courses = run_response.data
      this.run_courses.map(course => {
        course.reg_Enddate = convertDate(course.reg_Enddate)
        course.reg_Startdate = convertDate(course.reg_Startdate)
        course.run_Enddate = convertDate(course.run_Enddate)
        course.run_Startdate = convertDate(course.run_Startdate)
        course.reg_Endtime = convertTime(course.reg_Endtime)
        course.reg_Starttime = convertTime(course.reg_Starttime)
        course.run_Endtime = convertTime(course.run_Endtime)
        course.run_Starttime = convertTime(course.run_Starttime)
      }); 
      console.log(this.run_courses)
      let vote_response = await CourseService.searchUnvotedActiveInfo(null, null, null)
      console.log("vote_response", vote_response)
      this.vote_courses = vote_response.data
      console.log(this.vote_courses)
    } catch (error) {
      console.error("Error fetching course details:", error);
    }
  }
};
</script>

<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>