<template>
  <div>
    <ul class="nav nav-pills justify-content-center pt-5">
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

        <div class="container col-12">
          <h5 class="pb-3">Proposed Course</h5>
          <div v-if="pending_courses && pending_courses.length > 0" class="table-responsive">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'pending')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                   <th scope="col">
                      <a href="" @click.prevent="sort('proposed_Date', 'pending')" class="text-decoration-none text-dark">Proposed Date <sort-icon :sortColumn="sortColumn === 'proposed_Date'" :sortDirection="getSortDirection('proposed_Date')"/></a></th>
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('submitted_by', 'pending')">Owner <sort-icon :sortColumn="sortColumn === 'submitted_by'" :sortDirection="getSortDirection('submitted_by')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col" colspan="2">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(pending_course, key) in displayedPendingCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="pending_course.course_Name" :category="pending_course.coursecat_Name" :description="pending_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="proposed_date">
                          <course-date :date="pending_course.proposed_Date"></course-date>
                        </td>
                  <td class="submitted_by">
                    {{ pending_course.submitted_by }}
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(pending_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td>
                    <div class="action-buttons">
                      <course-action status="pending_approve" :id="pending_course.course_ID" @click="editCourse(pending_course.course_ID, 'approve')"></course-action>
                      <course-action status="pending_reject" :id="pending_course.course_ID" @click="openReject(pending_course)" data-bs-toggle="modal" data-bs-target="#rejected_modal"></course-action>
                    </div>
                  </td>                  
                </tr>
              </tbody>
            </table>
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
        course-name-placeholder="Course Name"
        @search-complete="handleSearchComplete2" />

        <div class="container col-12">
          <h5 class="pb-3">All Proposals</h5>
          <div class="table-responsive" v-if="proposed_courses && proposed_courses.length > 0">
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
                </tr>
              </thead>
              <tbody>
                <tr v-for="(proposed_course, key) in displayedProposedCourses" :key="key">
                  <td class="name">
                    <course-name-desc :name="proposed_course.course_Name" :category="proposed_course.coursecat_Name" :description="proposed_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="submitted_by_name text-nowrap">
                    {{ proposed_course.submitted_by_name }}
                  </td>
                  <td class="pl-0 border-top">
                    <course-status :status="proposed_course.pcourse_Status"></course-status>
                  </td>
                  <td v-if="proposed_course.reason === 'NULL' || proposed_course.reason === null " class="text-center">-</td>
                  <td v-else-if="proposed_course.reason !== NULL">{{ proposed_course.reason }}</td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(proposed_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
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

    <div class="modal fade" id="rejected_modal" tabindex="-1" aria-hidden="true" ref="rejectedModal">
      <div class="modal-dialog modal-lg"><reject-proposal-modal ref="rejectComponent"  id="after_action_modal" :course="rejectedCourse" @close-modal="closeReject"/></div>
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
import courseDate from '@/components/course/courseDate.vue';
import CommonService from "@/api/services/CommonService.js";
import UserService from "@/api/services/UserService.js";
import courseStatus from '../../components/course/courseStatus.vue';

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    rejectProposalModal,
    courseNameDesc,
    SearchFilter,
    CommonSearchFilter,
    courseDate,
    courseStatus
  },
  data() {
    return {
      proposed_courses: [],
      pending_courses: [],
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      rejectedCourse: null,
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
    openReject(course) {
      this.rejectedCourse = course;
      this.showModal = true;
      this.$refs.rejectComponent.resetData();
    },
    closeReject() {
      this.rejectedCourse = null;
      this.showModal = false;
    },
    async handleSearchComplete(searchResults) {
      this.pending_courses = searchResults;
    },
    async searchAllSubmittedProposedCoursesAdmin(course_Name, coursecat_ID) {
      try {
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
      this.proposed_courses = searchResults;
    },
    async searchAllApprovedRejectedProposedCoursesAdmin(course_Name, coursecat_ID, status) {
      try {
        let response = await CourseService.searchAllApprovedRejectedProposedCoursesAdmin(
          course_Name,
          coursecat_ID,
          status
        );
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
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.pending_courses)
         if (sort_response.code == 200) {
          this.pending_courses = sort_response.data
         }
      }
      if (action == 'proposed') {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.proposed_courses)
         if (sort_response.code == 200) {
          this.proposed_courses = sort_response.data
         }
      }
    },
    editCourse(courseId, action) {
      this.$router.push({ name: 'editProposedCourse', params: { courseId, action } });
    },
    modalRejectedClose() {
      this.loadData();
    },
    async loadData() {
      try {
        let pending_response = await CourseService.searchAllSubmittedProposedCoursesAdmin(null, null)
        this.pending_courses = pending_response.data
        
        let proposed_response = await CourseService.searchAllApprovedRejectedProposedCoursesAdmin(null, null, null)
        this.proposed_courses = proposed_response.data
        console.log(this.proposed_courses)
      } catch (error) {
        console.error("Error fetching course details:", error);
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
    document.title = "Propose Course DB | Upskilling Engagement System";

    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);
    if (role == 'Student') {
      this.$router.push({ name: 'studentViewCourse' }); 
    } else if (role == 'Instructor' || role == 'Trainer') {
        this.$router.push({ name: 'instructorTrainerViewVotingCampaign' });
    }else {
      this.loadData();
    }
  },
  mounted() {
    const buttonElement = document.createElement('button');
    buttonElement.className = 'btn btn-primary d-none invisible-btn';
    buttonElement.setAttribute('data-bs-toggle', 'modal');
    buttonElement.setAttribute('data-bs-target', '#rejected_modal');
    this.$el.appendChild(buttonElement);
    const modalElement = this.$refs.rejectedModal;
    modalElement.addEventListener('hidden.bs.modal', this.modalRejectedClose);
  },
  beforeUnmount() {
    const modalElement = this.$refs.rejectedModal;
    modalElement.removeEventListener('hidden.bs.modal', this.modalRejectedClose)
  }
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>