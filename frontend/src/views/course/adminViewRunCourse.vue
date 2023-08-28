<template>
  <div>
    <search-filter
      :status-options="statusOptions"
      :search-api="searchAllCoursesAdmin" 
      @search-complete="handleSearchComplete" />
    <div class="container col-12 table-responsive">
      <h5 class="pb-3">All Run Courses</h5>
      <div v-if="courses && courses.length > 0">
        <table class="table">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Registration Count <sort-icon :sortColumn="sortColumn === 'reg_count'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'status'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">Feedback Analysis</th>
              <th scope="col">Course Details</th>
              <th scope="col">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, key) in displayedCourses" :key="key">
              <td class="name">
                <course-name-desc :name="course.course_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
              </td>
              <td class="reg_count">
                {{ course.registration_count }}
              </td>
              <td class="closing_date">
                <course-date-time :date="course.reg_Enddate" :time="course.reg_Endtime"></course-date-time>
              </td>
              <td>{{ course.course_Status }}</td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis">View Feedback Analysis</a></td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
              <div class="row d-flex flex-nowrap">
                <td class="col row mx-1" v-if="course.course_Status === 'Active'"><course-action status="Deactivate" :id="course.course_ID"></course-action></td>
                <td class="col row mx-1" v-else-if="course.course_Status === 'Inactive'"><course-action status="Activate" :id="course.course_ID"></course-action></td>
                <td class="col row mx-1" v-else><course-action :status="course.course_Status" :id="course.course_ID"></course-action></td>
                <td class="col row mr-1"><course-action status="Edit" :id="course.course_ID"></course-action></td>
                <td class="col row mx-1"><course-action status="Delete" :id="course.course_ID"></course-action></td>
              </div>
            </tr>
          </tbody>
        </table>
        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" :status="selectedCourse.course_Status" @close-modal="closeModal" /></div>
        </div>
      </div>
      <div v-else-if="courses=[]">
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-if="courses.length/itemsPerPage > 0" v-model="localCurrentPageCourses" :totalItems="courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeCourses" class="justify-content-center pagination-container"/>
  </div>
</template>
  
<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import courseDateTime from '../../components/course/courseDateTime.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/AdminCommonSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";
import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    courseDateTime,
    SearchFilter
  },
  data() {
    return {
      courses: [],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageCourses: 1,
      statusOptions: ["Active", "Inactive", "Retired"],
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
    handlePageChangeCourses(newPage) {
      this.localCurrentPageCourses = newPage;
      this.$emit('page-change', newPage);
    },
    async handleSearchComplete(searchResults) {
      console.log("searchResults", searchResults);
      this.courses = searchResults; // Always update the courses array
      
    },
    async searchAllCoursesAdmin(user_ID, course_Name, coursecat_ID, status) {
      try {
        let response = await CourseService.searchAllCoursesAdmin(
          user_ID,
          course_Name,
          coursecat_ID,
          status
        );
        this.courses = response.data;
        
        return this.courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    }
  },
  computed: {
    displayedCourses() {
      const startIndex = (this.localCurrentPageCourses - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.courses.slice(startIndex, endIndex);
    },
  },
  async created() {
    try {
      let response = await CourseService.searchAllCoursesAdmin(null, null, null)
      this.courses = response.data
      this.courses.map(course => {
        course.reg_Enddate = convertDate(course.reg_Enddate)
        course.reg_Startdate = convertDate(course.reg_Startdate)
        course.run_Enddate = convertDate(course.run_Enddate)
        course.run_Startdate = convertDate(course.run_Startdate)
        course.reg_Endtime = convertTime(course.reg_Endtime)
        course.reg_Starttime = convertTime(course.reg_Starttime)
        course.run_Endtime = convertTime(course.run_Endtime)
        course.run_Starttime = convertTime(course.run_Starttime)
      }); 
    } catch (error) {
      console.error("Error fetching course details:", error);
    }
  },
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>