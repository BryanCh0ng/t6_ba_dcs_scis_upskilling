<template>
  <div>
    <ul class="nav nav-pills justify-content-center pt-5">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'allvote' }" @click="activeTab = 'allvote'">Voting Campaign Courses</a>
      </li> 
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'deleted' }" @click="activeTab = 'deleted'">Deleted Course(s)</a>
      </li>
    </ul>
    <div class="tab-content mt-5">
        <!-- all vote -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'allvote' }">
             <search-filter
              :status-options="statusOptions"
              :search-api="searchAllVotingCoursesAdmin"
              course-name-placeholder="Course Name"
              @search-complete="handleSearchComplete" />

            <div class="container col-12">
              <h5 class="pb-3">Courses Available for Students to Indicate Interest</h5>
              <div v-if="vote_courses && vote_courses.length > 0" class="table-responsive">
                <table class="table bg-white">
                  <thead>
                    <tr class="text-nowrap">
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'allvote')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                    <th scope="col">
                        <a href="" @click.prevent="sort('proposed_Date', 'allvote')" class="text-decoration-none text-dark">Propose Date <sort-icon :sortColumn="sortColumn === 'proposed_Date'" :sortDirection="getSortDirection('proposed_Date')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('voteCount', 'allvote')"># of Interest <sort-icon :sortColumn="sortColumn === 'voteCount'" :sortDirection="getSortDirection('voteCount')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('vote_Status', 'allvote')">Status <sort-icon :sortColumn="sortColumn === 'vote_Status'" :sortDirection="getSortDirection('vote_Status')"/></a></th>
                    <th scope="col">Course Details</th>
                    <th scope="col">Action(s)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(vote_course, key) in displayedVoteCourses" :key="key">
                    <td class="name">
                      <course-name-desc :name="vote_course.course_Name" :category="vote_course.coursecat_Name" :description="vote_course.course_Desc"></course-name-desc>
                    </td>
                    <td class="proposed_date">
                      <course-date :date="vote_course.proposed_Date"></course-date>
                    </td>
                    <td class="current_interest">
                        {{ vote_course.voteCount }}
                    </td>
                    <td class="pl-0 border-top">
                      <course-status v-if="vote_status" :status="vote_status[vote_course.vote_Status]"></course-status>
                    </td>
                    <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(vote_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                    <td v-if="vote_course && vote_course.vote_Status === 'Ongoing'">
                      <div class="action-buttons">
                        <course-action status="Close" @action-and-message-updated="handleActionData" :course="vote_course"></course-action>
                      </div>
                    </td>
                    <td v-else-if="vote_course && vote_course.vote_Status === 'Closed'">
                      <div class="action-buttons">
                        <course-action status="promote_to_course" @action-and-message-updated="handleActionData" :course="vote_course"></course-action>
                        <course-action @action-and-message-updated="handleActionData" status="unoffered-vote" :course="vote_course"></course-action>
                      </div>
                    </td>
                    <td v-else></td>
                  </tr>
                  </tbody>
                </table>
              </div>
              <div v-else-if="vote_courses=[]">
                <p>No records found</p>
              </div>
            </div>
            <vue-awesome-paginate v-model="localCurrentPage" :totalItems="vote_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
        </div>

      <!-- deleted -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'deleted' }">
             <proposal-course-related-search-filter
              :search-api="searchAllNotOfferedVotingCoursesAdmin"
              @search-complete="handleSearchCompleteNotOffered" />

            <div class="container col-12">
              <h5 class="pb-3">Courses Available that has low number of interest</h5>
              <div class="table-responsive" v-if="notoffered_courses && notoffered_courses.length > 0">
                <table class="table bg-white">
                  <thead>
                    <tr class="text-nowrap">
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'deleted')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                    <th scope="col">
                        <a href="" @click.prevent="sort('proposed_Date', 'deleted')" class="text-decoration-none text-dark">Propose Date <sort-icon :sortColumn="sortColumn === 'proposed_Date'" :sortDirection="getSortDirection('proposed_Date')"/></a></th>
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('voteCount', 'deleted')"># of Interest <sort-icon :sortColumn="sortColumn === 'voteCount'" :sortDirection="getSortDirection('voteCount')"/></a></th>
                    <th scope="col">Course Details</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(notoffered_course, key) in displayedNotOfferedCourses" :key="key">
                    <td class="name">
                      <course-name-desc :name="notoffered_course.course_Name" :category="notoffered_course.coursecat_Name" :description="notoffered_course.course_Desc"></course-name-desc>
                    </td>
                    <td class="proposed_date">
                      <course-date :date="notoffered_course.proposed_Date"></course-date>
                    </td>
                    <td class="current_interest">
                        {{ notoffered_course.voteCount }}
                    </td>
                    <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(notoffered_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  </tr>
                  </tbody>
                </table>
              </div>
              <div v-else-if="notoffered_courses=[]">
                <p>No records found</p>
              </div>
            </div>
            <vue-awesome-paginate v-model="localCurrentPage" :totalItems="notoffered_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
        </div>
      
    </div>
    <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
    </div>

    <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
      <div class="modal-dialog modal-lg"> 
        <modal-after-action :course="actionCourse" @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal" />
      </div>
    </div>
      
  </div>
</template>
    
<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import courseDate from '@/components/course/courseDate.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/AdminCommonSearchFilter.vue";
import ProposalCourseRelatedSearchFilter from "@/components/search/ProposalCourseRelatedSearchFilter.vue";
import UserService from "@/api/services/UserService.js";
import CourseService from "@/api/services/CourseService.js";
import modalAfterAction from '@/components/course/modalAfterAction.vue';
import CommonService from "@/api/services/CommonService.js";
import courseStatus from '../../components/course/courseStatus.vue';

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    SearchFilter,
    courseDate,
    modalAfterAction,
    ProposalCourseRelatedSearchFilter,
    courseStatus
  },

  data() {
    return {
        vote_courses: [],
        notoffered_courses: [],
        sortColumn: '',
        sortDirection: 'asc',
        selectedCourse: null,
        itemsPerPage: 10,
        localCurrentPage: 1,
        localCurrentPageNotOffered: 1,
        activeTab: 'allvote',
        statusOptions: ["Open for voting", "Offered for students to register", "Voting closed for students"],
        actionCourse: {},
        vote_status: {
          "Ongoing": "Open for voting",
          "Offered": "Offered for students to register",
          "Closed": "Voting closed for students"
        },
        search_vote_status: null,
        search_course_name: null,
        search_course_category: null
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
    handlePageChangeNotOffered(newPage) {
      this.localCurrentPage = newPage;
      this.$emit('page-change', newPage);
    },
    handleActionData(actionData) {
      this.receivedMessage = actionData.message;
      this.actionCourse = actionData.course
      const modalButtonElement = this.$el.querySelector('.invisible-btn')
      modalButtonElement.click();
    },
    modalAfterActionClose() {
      this.loadData();
    },
    async handleSearchComplete(searchResults) {
      this.vote_courses = searchResults; 
    },
    async handleSearchCompleteNotOffered(searchResults) {
      this.notoffered_courses = searchResults; 
    },
    async searchAllVotingCoursesAdmin(course_Name, coursecat_ID, vote_status) {
      this.search_course_name = course_Name
      this.search_course_category = coursecat_ID
      // this.vote_status = vote_status

      if (vote_status == "Open for voting") {
        vote_status = "Ongoing"
      } else if (vote_status == "Offered for students to register") {
        vote_status = "Offered"
      } else if (vote_status == "Voting closed for students") {
        vote_status = "Closed"
      }

      try {
        let response = await CourseService.searchAllVotingCoursesAdmin(
          course_Name,
          coursecat_ID,
          vote_status
        );
        this.vote_courses = response.data;
        return this.vote_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },
    async searchAllNotOfferedVotingCoursesAdmin(course_Name, coursecat_ID) {
      this.search_course_name = course_Name
      this.search_course_category = coursecat_ID
      try {
        let response = await CourseService.searchAllNotOfferedVotingCoursesAdmin(
          course_Name,
          coursecat_ID,
        );
        this.notoffered_courses = response.data;
        return this.notoffered_courses;
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
      if (action == "allvote") {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.vote_courses)
        if (sort_response.code == 200) {
          this.vote_courses = sort_response.data
        }
      }
     if (action == "deleted") {
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.notoffered_courses)
        if (sort_response.code == 200) {
          this.notoffered_courses = sort_response.data
        }
      }
    },
    async loadData() {
      let response = await CourseService.searchAllVotingCoursesAdmin(this.search_course_name, this.search_course_category, this.search_vote_status)
      this.vote_courses = response.data

      let course = await CourseService.searchAllNotOfferedVotingCoursesAdmin(this.search_course_name, this.search_course_category)
      this.notoffered_courses = course.data
    }
  },
  computed: {
    displayedVoteCourses() {
      const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.vote_courses.slice(startIndex, endIndex);
    },

    displayedNotOfferedCourses() {
      const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.notoffered_courses.slice(startIndex, endIndex);
    }
  },
  async created() {
    document.title = "Voting Campaign DB | Upskilling Engagement System";

    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);
    if (role == 'Student') {
      this.$router.push({ name: 'studentViewCourse' }); 
    } else if (role == 'Instructor' || role == 'Trainer') {
      this.$router.push({ name: 'instructorTrainerViewVotingCampaign' });
    }else {
      try {
        let response = await CourseService.searchAllVotingCoursesAdmin(null, null, null)
        this.vote_courses = response.data

        let course = await CourseService.searchAllNotOfferedVotingCoursesAdmin(null, null)
        this.notoffered_courses = course.data
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    }
  },
  mounted() {
    const buttonElement = document.createElement('button');
    buttonElement.className = 'btn btn-primary d-none invisible-btn';
    buttonElement.setAttribute('data-bs-toggle', 'modal');
    buttonElement.setAttribute('data-bs-target', '#after_action_modal');
    this.$el.appendChild(buttonElement);
    const modalElement = this.$refs.afterActionModal;
    modalElement.addEventListener('hidden.bs.modal', this.modalAfterActionClose);
  },
  beforeUnmount() {
    const modalElement = this.$refs.afterActionModal;
    modalElement.removeEventListener('hidden.bs.modal', this.modalAfterActionClose)
  }
}
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>