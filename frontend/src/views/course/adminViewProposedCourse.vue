<template>
  <div>
    <ul class="nav nav-pills justify-content-center">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'submitted' }" @click="activeTab = 'submitted'">Submitted</a>
      </li> 
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'approved_rejected' }" @click="activeTab = 'approved_rejected'">Approved/Rejected</a>
      </li>
    </ul>
    <div class="tab-content ">
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'submitted' }">
        <search-filter
        :status-options="statusOptions"
        :search-api="searchAllPendingCoursesAdmin"
        @search-complete="handleSearchComplete" />
        <div class="container col-12 table-responsive">
          <h5 class="pb-3">Proposed Course</h5>
          <div v-if="pending_courses.length > 0">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Owner <sort-icon :sortColumn="sortColumn === 'owner'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Proposed Date <sort-icon :sortColumn="sortColumn === 'proposed_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(pending_course, key) in displayedPendingCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="pending_course.course_Name" :category="pending_course.coursecat_Name" :description="pending_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="submitted_by_name">
                    {{ pending_course.submitted_by }}
                  </td>
                  <td class="closing_date">
                    <div class="col-12">
                      {{ pending_course.proposed_date }}
                    </div>
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(pending_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action status="pending_approve" :course="pending_course"></course-action></td>
                  <td><course-action status="pending_reject" :course="pending_course" @click="openReject(pending_course)" data-bs-toggle="modal" data-bs-target="#rejected_modal"></course-action></td>
                </tr>
              </tbody>
            </table>
            <div class="modal fade" id="rejected_modal" tabindex="-1" aria-hidden="true">
              <div class="modal-dialog modal-lg"><reject-proposal-modal @close-modal="closeReject"/></div>
            </div>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="pending_courses.length/itemsPerPage > 0" v-model="localCurrentPagePending" :totalItems="pending_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangePending" class="justify-content-center pagination-container"/>
      </div>
      
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'approved_rejected' }">
        <common-search-filter
        :search-api="searchAllProposedCoursesAdmin"
        @search-complete="handleSearchComplete" />
        <div class="container col-12 table-responsive">
          <h5 class="pb-3">All Proposals</h5>
          <div v-if="proposed_courses.length > 0">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Owner <sort-icon :sortColumn="sortColumn === 'owner'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Proposed Date <sort-icon :sortColumn="sortColumn === 'proposed_date'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'status'" :sortDirection="sortDirection"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(proposed_course, key) in displayedProposedCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="proposed_course.course_Name" :category="proposed_course.coursecat_Name" :description="proposed_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="reg_count">
                    {{ proposed_course.submitted_by_name }}
                  </td>
                  <td class="closing_date">
                    <div class="col-12">
                      {{ proposed_course.proposed_date }}
                    </div>
                  </td>
                  <td>{{ proposed_course.pcourse_Status }}</td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(proposed_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action :status="proposed_course.pcourse_Status" :course="proposed_course"></course-action></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="proposed_courses.length/itemsPerPage > 0" v-model="localCurrentPageProposed" :totalItems="proposed_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeProposed" class="justify-content-center pagination-container"/>
      </div>
    </div>
    <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
    </div>
  </div>
</template>
    
<script>
import courseAction from '@/components/course/courseAction.vue';
import sortIcon from '@/components/common/sort-icon.vue';
import modalCourseContent from '@/components/course/modalCourseContent.vue';
import rejectProposalModal from '@/components/course/rejectProposalModal.vue';
import courseNameDesc from '@/components/course/courseNameDesc.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/CourseRelatedSearchFilter.vue";
import CommonSearchFilter from "@/components/search/CommonSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    rejectProposalModal,
    courseNameDesc,
    SearchFilter,
    CommonSearchFilter
  },
  data() {
    return {
      proposed_courses: [],
      pending_courses: [],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPagePending: 1,
      localCurrentPageProposed: 1,
      activeTab: 'submitted'
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
    handlePageChangePending(newPage) {
      this.localCurrentPagePending = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeProposed(newPage) {
      this.localCurrentPageProposed = newPage;
      this.$emit('page-change', newPage);
    },
    openReject() {
      this.showModal = true;
    },
    closeReject() {
      this.showModal = false;
    },
    async handleSearchComplete(searchResults) {
      console.log(searchResults)
      this.courses = searchResults;
    },
    async searchAllPendingCoursesAdmin(user_ID, course_Name, coursecat_ID, status) {
      try {
        let response = await CourseService.searchInstructorProposedCourseInfo(
          user_ID,
          course_Name,
          coursecat_ID,
          status
        );
        this.vote_courses = response.data;
        return this.vote_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    async searchAllProposedCoursesAdmin(user_ID, course_Name, coursecat_ID, status) {
      try {
        let response = await CourseService.searchInstructorProposedCourseInfo(
          user_ID,
          course_Name,
          coursecat_ID,
          status
        );
        this.vote_courses = response.data;
        return this.vote_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    }
  },
  computed: {
    displayedPendingCourses() {
      const startIndex = (this.localCurrentPagePending - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.pending_courses.slice(startIndex, endIndex);
    },
    displayedProposedCourses() {
      const startIndex = (this.localCurrentPageProposed - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.proposed_courses.slice(startIndex, endIndex);
    }
  },
  async created() {
    try {
      let pending_response = await CourseService.searchAllSubmittedProposedCoursesAdmin(null, null)
      this.pending_courses = pending_response.data
      console.log(pending_response)
      let proposed_response = await CourseService.searchAllApprovedRejectedProposedCoursesAdmin(null, null, null)
      this.proposed_courses = proposed_response.data
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