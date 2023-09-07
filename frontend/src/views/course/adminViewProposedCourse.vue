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
        :search-api="searchAllSubmittedProposedCoursesAdmin"
        @search-complete="handleSearchComplete" />

        <div class="container col-12 table-responsive">
          <h5 class="pb-3">Proposed Course</h5>
          <div v-if="pending_courses && pending_courses.length > 0">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'pending')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('submitted_by', 'pending')">Owner <sort-icon :sortColumn="sortColumn === 'submitted_by'" :sortDirection="getSortDirection('submitted_by')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(pending_course, key) in displayedPendingCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="pending_course.course_Name" :category="pending_course.coursecat_Name" :description="pending_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="submitted_by">
                    {{ pending_course.submitted_by }}
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(pending_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td><course-action status="pending_approve" :id="pending_course.course_ID" @click="editCourse(pending_course.course_ID)"></course-action></td>
                  <td><course-action status="pending_reject" :id="pending_course.course_ID" @click="openReject(pending_course)" data-bs-toggle="modal" data-bs-target="#rejected_modal"></course-action></td>
                </tr>
              </tbody>
            </table>
            <div class="modal fade" id="rejected_modal" tabindex="-1" aria-hidden="true">
              <div class="modal-dialog modal-lg"><reject-proposal-modal @close-modal="closeReject"/></div>
            </div>
          </div>
          <div v-else-if="pending_courses=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="pending_courses.length/itemsPerPage > 0" v-model="localCurrentPagePending" :totalItems="pending_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangePending" class="justify-content-center pagination-container"/>
      </div>

      <!-- Approved Rejected -->
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'approved_rejected' }">
        <common-search-filter class="mt-5"
        :status-options="statusOptions"
        :search-api="searchAllApprovedRejectedProposedCoursesAdmin"
        @search-complete="handleSearchComplete2" />

        <div class="container col-12 table-responsive">
          <h5 class="pb-3">All Proposals</h5>
          <div  v-if="proposed_courses && proposed_courses.length > 0">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" @click.prevent="sort('course_Name', 'proposed')" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                  <th scope="col">
                    <a href="" @click.prevent="sort('submitted_by_name', 'proposed')" class="text-decoration-none text-dark">Owner <sort-icon :sortColumn="sortColumn === 'submitted_by_name'" :sortDirection="getSortDirection('submitted_by_name')"/></a></th>
                  <th scope="col">
                    <a href="" @click.prevent="sort('pcourse_Status', 'proposed')" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'pcourse_Status'" :sortDirection="getSortDirection('pcourse_Status')"/></a></th>
                  <th scope="col">Rejection Reason</th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(proposed_course, key) in displayedProposedCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="proposed_course.course_Name" :category="proposed_course.coursecat_Name" :description="proposed_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="submitted_by_name">
                    {{ proposed_course.submitted_by_name }}
                  </td>
                  <td>{{ proposed_course.pcourse_Status }}</td>
                  <td>{{ proposed_course.reason }}</td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(proposed_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <!-- <td><course-action :status="proposed_course.pcourse_Status" :id="proposed_course.course_ID"></course-action></td> -->
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="proposed_courses=[]">
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
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import rejectProposalModal from '../../components/course/rejectProposalModal.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/ProposalCourseRelatedSearchFilter.vue";
import CommonSearchFilter from "@/components/search/AdminCommonSearchFilter.vue";
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
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPagePending: 1,
      localCurrentPageProposed: 1,
      activeTab: 'submitted',
      statusOptions: ["Approved", "Rejected"],
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
      // console.log(searchResults)
      this.pending_courses = searchResults;
    },
    async searchAllSubmittedProposedCoursesAdmin(course_Name, coursecat_ID) {
      try {
        console.log(coursecat_ID)
        let response = await CourseService.searchAllSubmittedProposedCoursesAdmin(
          course_Name,
          coursecat_ID
        );
        this.pending_courses = response.data;
        return this.pending_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
     async handleSearchComplete2(searchResults) {
      // console.log(searchResults)
      this.proposed_courses = searchResults;
    },
    async searchAllApprovedRejectedProposedCoursesAdmin(course_Name, coursecat_ID, status) {
      try {
        console.log(status)
        let response = await CourseService.searchAllApprovedRejectedProposedCoursesAdmin(
          course_Name,
          coursecat_ID,
          status
        );
        console.log(response.data)
        this.proposed_courses = response.data;
        return this.proposed_courses;
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
    async sortCourse(action) {
      if (action == 'pending') {
        let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.pending_courses)
         if (sort_response.code == 200) {
          this.pending_courses = sort_response.data
         }
      }
      if (action == 'proposed') {
        let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.proposed_courses)
         if (sort_response.code == 200) {
          this.proposed_courses = sort_response.data
         }
      }
    },
    editCourse(courseId) {
      this.$router.push({ name: 'editProposedCourse', params: { courseId } });
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