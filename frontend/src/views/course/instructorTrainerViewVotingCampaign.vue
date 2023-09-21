<template>
  <div>
    <search-filter
      :search-api="searchAllOngoingVoteCourse" 
      @search-complete="handleSearchComplete" />

    <div class="container col-12">
      <h5 class="pb-3">Courses Available for Students to Indicate Interest</h5>
      <div v-if="courses && courses.length > 0" class="table-responsive">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" @click.prevent="sort('course_Name')" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
              <th scope="col">
                <a href="" @click.prevent="sort('voteCount')" class="text-decoration-none text-dark"># of Interest <sort-icon :sortColumn="sortColumn === 'voteCount'" :sortDirection="getSortDirection('voteCount')"/></a></th>
              <th scope="col">Course Details</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, key) in displayedCourses" :key="key">
              <td class="name">
                <course-name-desc :name="course.course_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
              </td>
              <td class="reg_count">
                {{ course.voteCount }}
              </td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
            </tr>               
          </tbody>
        </table>
        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
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
import sortIcon from '@/components/common/sort-icon.vue';
import modalCourseContent from '@/components/course/modalCourseContent.vue';
import courseNameDesc from '@/components/course/courseNameDesc.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/ProposalCourseRelatedSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";

export default {
  components: {
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    SearchFilter
  },
  data() {
    return {
      courses: [],
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageCourses: 1,
    }
  },
  computed: {
    displayedCourses() {
      const startIndex = (this.localCurrentPageCourses - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.courses.slice(startIndex, endIndex);
    },
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
      this.courses = searchResults;
      
    },
    async searchAllOngoingVoteCourse(courseName, coursecat_ID) {
      try {
        let response = await CourseService.searchAllVotingCoursesAdmin(courseName, coursecat_ID, 'Ongoing');
        this.courses = response.data;
        
        return this.courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    async loadData() {
      try {
        let response = await CourseService.searchAllVotingCoursesAdmin(null, null, 'Ongoing')
        console.log(response)
        this.courses = response.data
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    },
    sort(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortColumn = column;
        this.sortDirection = 'asc';
      }
      this.sortCourse()
    },
    getSortDirection(column) {
      if (this.sortColumn === column) {
        return this.sortDirection;
      }
    },
    async sortCourse() {
      let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.courses)
        if (sort_response.code == 200) {
          this.courses = sort_response.data
        }
    }
  },
  created() {
   this.loadData();
  }
  }
</script>

<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>