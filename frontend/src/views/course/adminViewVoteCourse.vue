<template>
  <div>
    <search-filter
      :status-options="statusOptions"
      :search-api="searchAllVotingCoursesAdmin"
      @search-complete="handleSearchComplete" />

    <div class="container col-12 table-responsive">
      <h5 class="pb-3">Courses Available for Students to Indicate Interest</h5>
      <div v-if="vote_courses.length > 0">
        <table class="table">
          <thead>
            <tr class="text-nowrap">
            <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
            <th scope="col">
                <a href="" class="text-decoration-none text-dark"># of Current Interest <sort-icon :sortColumn="sortColumn === 'reg_count'" :sortDirection="sortDirection"/></a></th>
            <th scope="col">
                <a href="" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'status'" :sortDirection="sortDirection"/></a></th>
            <th scope="col">Course Details</th>
            <th scope="col">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(vote_course, key) in displayedVoteCourses" :key="key">
            <td class="name">
              <course-name-desc :name="vote_course.course_Name" :category="vote_course.coursecat_Name" :description="vote_course.course_Desc"></course-name-desc>
            </td>
            <td class="current_interest">
                {{ vote_course.vote_Count }}
            </td>
            <td>{{ vote_course.vote_Status }}</td>
            <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(vote_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
            <td v-if="vote_course.vote_Status === 'Ongoing'"><course-action status="Close" :id="vote_course.course_ID"></course-action></td>
            <td v-else-if="vote_course.vote_Status === 'Closed'"><course-action status="Open for Registration" :id="vote_course.course_ID"></course-action></td>
            <td v-else><course-action status="Open for Voting" :id="vote_course.course_ID"></course-action></td>
          </tr>
          </tbody>
        </table>
        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
        </div>
      </div>
      <div v-else>
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-model="localCurrentPage" :totalItems="vote_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
  </div>
</template>
    
<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import SearchFilter from "@/components/search/AdminCommonSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    SearchFilter
  },
  data() {
    return {
      vote_courses: [],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPage: 1,
      statusOptions: ["Ongoing", "Offered", "Closed"],
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
    async handleSearchComplete(searchResults) {
      this.vote_courses = searchResults;
    },
    async searchAllVotingCoursesAdmin(course_Name, coursecat_ID, status) {
      console.log("vote status",status)
      try {
        let response = await CourseService.searchAllVotingCoursesAdmin(
          course_Name,
          coursecat_ID,
          status
        );
        console.log(response.data)
        this.vote_courses = response.data;
        return this.vote_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    }
  },
  computed: {
    displayedVoteCourses() {
      const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.vote_courses.slice(startIndex, endIndex);
    }
  },
  async created() {
    try {
      let response = await CourseService.searchAllVotingCoursesAdmin(null, null, null)
      console.log(response.data)
      this.vote_courses = response.data
      console.log(this.vote_courses)
    } catch (error) {
      console.error("Error fetching course details:", error);
    }
  }
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>