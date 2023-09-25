<template>
  <div>
    <ul class="nav nav-pills justify-content-center">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'registered' }" @click="activeTab = 'registered'">Registered</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'interested' }" @click="activeTab = 'interested'">Interested</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'proposed' }" @click="activeTab = 'proposed'">Proposed</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'completed' }" @click="activeTab = 'completed'">Completed</a>
      </li>
    </ul>
    <div class="tab-content ">
      <!-- registered -->
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'registered' }">
        <search-filter
            :status-options="statusOptionsRegistered"
            :search-api="searchCourseRegistrationInfo"
            @search-complete="handleSearchCompleteRegistered" />

        <div class="container col-12">
          <h5 class="pb-3">My Registered Course</h5>
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
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Enddate', 'registered')">Closing Date<sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
                    
                  <th scope="col">
                    <a href="" class="text-decoration-none text-dark" @click.prevent="sort('reg_Status', 'registered')">Status <sort-icon :sortColumn="sortColumn === 'reg_Status'" :sortDirection="getSortDirection('reg_Status')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
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
                  <td>
                    <course-date-time :date="registered_course.reg_Enddate" :time="registered_course.reg_Endtime"></course-date-time>
                  </td>
                  <td>
                    {{ registered_course.reg_Status }}
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(registered_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td v-if="(registered_course.reg_Status === 'Enrolled' || registered_course.reg_Status === 'Pending') && isClosingDateValid(registered_course.reg_Enddate)">
                      <course-action status="registered_drop" @action-and-message-updated="handleActionData" :course="registered_course"></course-action>
                  </td>
                </tr>
              </tbody>

            </table>

          </div>
          <div v-else-if="registered_courses=[] && onInitialEmptyRegistered">
            <div class="pt-5 text-center">
              <p>You have not yet enrolled in any courses.</p>
              <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Register for a Course</router-link>
            </div>
          </div>
          <div v-else-if="registered_courses=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="registered_courses.length/itemsPerPage > 0" v-model="localCurrentPageRegistered" :totalItems="registered_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeRegistered" class="justify-content-center pagination-container"/>
      </div>

      <!-- interested -->
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'interested' }">
        <search-filter
            :status-options="statusOptionsInterested"
            :search-api="searchCourseVoteInfo"
            @search-complete="handleSearchCompleteInterested" />

        <div class="container col-12">
          <h5 class="pb-3">My Interested Course</h5>
          <div v-if="interested_courses && interested_courses.length > 0" class="table-responsive">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" @click.prevent="sort('course_Name', 'interested')" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                  <th scope="col">
                    <a href="" @click.prevent="sort('vote_Status', 'interested')" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'vote_Status'" :sortDirection="getSortDirection('vote_Status')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(interested_course, key) in displayedInterestedCourses" :key="key">
                  <td>
                    <course-name-desc :name="interested_course.course_Name" :category="interested_course.coursecat_Name" :description="interested_course.course_Desc"></course-name-desc>
                  </td>
                  <td>
                    {{ interested_course.vote_Status }}
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(interested_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <td v-if="interested_course.vote_Status == 'Ongoing'">
                      <course-action @action-and-message-updated="handleActionData" status="say-pass" :course="interested_course"></course-action>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="interested_courses=[] && onInitialEmptyInterested">
            <div class="pt-5 text-center">
              <p>You have not yet expressed interest in any courses.</p>
              <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Indicate Interest</router-link>
              
            </div>
          </div>
          <div v-else-if="interested_courses=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="interested_courses.length/itemsPerPage > 0" v-model="localCurrentPageInterested" :totalItems="interested_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeInterested" class="justify-content-center pagination-container"/>
      </div>

      <!-- proposed -->
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'proposed' }">
        <search-filter
            :status-options="statusOptionsProposed"
            :search-api="searchProposedInfo"
            @search-complete="handleSearchCompleteProposed" />

        <div class="container col-12">
          <h5 class="pb-3">My Proposed Course</h5>
          <div  v-if="proposed_courses && proposed_courses.length > 0" class="table-responsive">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" @click.prevent="sort('course_Name', 'proposed')" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                  <th scope="col">
                      <a href="" @click.prevent="sort('proposed_Date', 'proposed')" class="text-decoration-none text-dark">Proposed Date <sort-icon :sortColumn="sortColumn === 'proposed_Date'" :sortDirection="getSortDirection('proposed_Date')"/></a></th>
                  <th scope="col">
                    <a href="" @click.prevent="sort('pcourse_Status', 'proposed')" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'pcourse_Status'" :sortDirection="getSortDirection('pcourse_Status')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(proposed_course, key) in displayedProposedCourses" :key="key">
                  <td>
                    <course-name-desc :name="proposed_course.course_Name" :category="proposed_course.coursecat_Name" :description="proposed_course.course_Desc"></course-name-desc>
                  </td>
                  <td class="proposed_date">
                    <course-date :date="proposed_course.proposed_Date"></course-date>
                  </td>
                  <td>{{ proposed_course.pcourse_Status }}</td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(proposed_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <div v-if="proposed_course.pcourse_Status == 'Pending'">
                    <td><course-action status="Edit" :id="proposed_course.course_ID" @click="editCourse(proposed_course.course_ID)"></course-action></td>
                    <td><course-action @action-and-message-updated="handleActionData" status="remove-proposal" :course="proposed_course"></course-action></td>
                  </div>
                  <div v-else-if="proposed_course.pcourse_Status == 'Rejected'">
                    <td><course-action status="rejected-reason" @click="openRejectedCourseModal(proposed_course)" data-bs-toggle="modal" data-bs-target="#rejected_course_modal"></course-action></td>
                  </div>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="proposed_courses=[] && onInitialEmptyProposed">
            <div class="pt-5 text-center">
              <p>You have not yet proposed any courses.</p>
               <router-link :to="{ name: 'proposeCourse' }" class="btn btn-edit">Propose a Course</router-link>
            </div>
          </div>
          <div v-else-if="proposed_courses=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="proposed_courses.length/itemsPerPage > 0" v-model="localCurrentPageProposed" :totalItems="proposed_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeProposed" class="justify-content-center pagination-container"/>
      </div>

      <!-- completed -->
      <div class="tab-pane fade" :class="{ 'show active': activeTab === 'completed' }">
        <student-search-filter
            :search-api="searchCompletedInfo"
            @search-complete="handleSearchCompleteCompleted" />

        <div class="container col-12">
          <h5 class="pb-3">My Completed Courses</h5>
          <div  v-if="completed_courses && completed_courses.length > 0" class="table-responsive">
            <table class="table bg-white">
              <thead>
                <tr class="text-nowrap">
                  <th scope="col">
                    <a href="" @click.prevent="sort('course_Name', 'completed')" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                  <th scope="col">
                    <a href="" @click.prevent="sort('instructor_Name', 'completed')" class="text-decoration-none text-dark">Instructor Name <sort-icon :sortColumn="sortColumn === 'instructor_Name'" :sortDirection="getSortDirection('instructor_Name')"/></a></th>
                  <th scope="col">Course Details</th>
                  <th scope="col">Action(s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(completed_course, key) in displayedCompletedCourses" :key="key">
                  <td>
                    <course-name-desc :name="completed_course.course_Name" :category="completed_course.coursecat_Name" :description="completed_course.course_Desc"></course-name-desc>
                  </td>
                  <td>
                    {{ completed_course.instructor_Name }}
                  </td>
                  <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(completed_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                  <div v-if="completed_course.feedback_submitted == true">
                    <td><course-action status="view-feedback" :id="completed_course.course_ID"></course-action></td>
                  </div>
                  <div v-else>
                    <td><course-action status="provide-feedback" :id="completed_course.course_ID"></course-action></td>
                  </div>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else-if="completed_courses=[] && onInitialEmptyCompleted">
            <div class="pt-5 text-center">
              <p>You have not yet completed any courses.</p>
              <router-link :to="{ name: 'studentViewCourse' }" class="btn btn-edit">Register for a Course</router-link>
            </div>
          </div>
          <div v-else-if="completed_courses=[]">
            <p>No records found</p>
          </div>
        </div>
        <vue-awesome-paginate v-if="completed_courses.length/itemsPerPage > 0" v-model="localCurrentPageCompleted" :totalItems="completed_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeCompleted" class="justify-content-center pagination-container"/>
      </div>

      <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" />
        </div>
      </div>

      <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
        <div class="modal-dialog modal-lg"> 
          <modal-after-action :course="actionCourse" @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal" />
        </div>
      </div>
      
      <div class="modal fade" id="rejected_course_modal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <modal-rejected-reason
            v-if="showRejectedCourseModal"
            :course="selectedRejectedCourse"
            :message="receivedRejectedCourseMessage"
            @close-modal="closeRejectedCourseModal"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import courseDateTime from '@/components/course/courseDateTime.vue';
import courseDate from '@/components/course/courseDate.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/CommonSearchFilter.vue";
import StudentSearchFilter from "@/components/search/StudentCourseSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";
// import UserService from "@/api/services/UserService.js";
import modalAfterAction from '@/components/course/modalAfterAction.vue';
import modalRejectedReason from '@/components/course/modalRejectedReason.vue';

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc,
    SearchFilter,
    StudentSearchFilter,
    courseDateTime,
    modalAfterAction,
    modalRejectedReason,
    courseDate,
  },
  data() {
    return {
      registered_courses: [],
      interested_courses: [],
      proposed_courses: [],
      completed_courses: [],
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageRegistered: 1,
      localCurrentPageInterested: 1,
      localCurrentPageProposed: 1,
      localCurrentPageCompleted: 1,
      activeTab: 'registered',
      statusOptionsRegistered: ["Enrolled", "Pending", "Not Enrolled", "Dropped"],
      statusOptionsInterested: ["Offered", "Ongoing", "Closed"],
      statusOptionsProposed: ["Approved", "Rejected", "Pending"],
      currentDate: new Date(),
      user_ID: 1,
      onInitialEmptyRegistered: false,
      onInitialEmptyInterested: false,
      onInitialEmptyProposed: false,
      onInitialEmptyCompleted: false,
      receivedMessage: '',
      actionCourse: {},
      showRejectedCourseModal: false,
      selectedRejectedCourse: null,
      receivedRejectedCourseMessage: '',
    }
  },
  methods: {
    async get_user_id() {
      try {
        const user_ID = await UserService.getUserID()
        this.user_ID = user_ID

      } catch (error) {
        this.message = error.message
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
    handleActionData(actionData) {
      this.receivedMessage = actionData.message;
      this.actionCourse = actionData.course
      const modalButtonElement = this.$el.querySelector('.invisible-btn')
      modalButtonElement.click();
    },
    modalAfterActionClose() {
      this.loadData();
    },
    openRejectedCourseModal(proposedCourse) {
      this.selectedRejectedCourse = proposedCourse;
      this.showRejectedCourseModal = true;
      this.receivedRejectedCourseMessage = proposedCourse.reason;
    },

    closeRejectedCourseModal() {
      this.selectedRejectedCourse = null;
      this.showRejectedCourseModal = false;
      this.receivedRejectedCourseMessage = '';
    },
    handlePageChangeRegistered(newPage) {
      this.localCurrentPageRegistered = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeInterested(newPage) {
      this.localCurrentPageInterested = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeProposed(newPage) {
      this.localCurrentPageProposed = newPage;
      this.$emit('page-change', newPage);
    },
    handlePageChangeCompleted(newPage) {
      this.localCurrentPageCompleted = newPage;
      this.$emit('page-change', newPage);
    },
    async handleSearchCompleteRegistered(searchResults) {
      this.registered_courses = searchResults;
    },

    async handleSearchCompleteInterested(searchResults) {
      this.interested_courses = searchResults;
    },

    async handleSearchCompleteProposed(searchResults) {
      this.proposed_courses = searchResults;
    },

    async handleSearchCompleteCompleted(searchResults) {
      this.completed_courses = searchResults;
    },
    async searchCourseRegistrationInfo(user_ID, course_Name, coursecat_ID, status) {
      try {
        // let user_id = await UserService.getUserID()
        let user_id = 1 
        user_ID = user_id

        let response = await CourseService.searchCourseRegistrationInfo(
          user_ID,
          course_Name,
          coursecat_ID,
          status
        );
        this.registered_courses = response.data;
        // console.log(this.registered_courses)
        return this.registered_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },

    async searchCourseVoteInfo(user_ID, course_Name, coursecat_ID, status) {
      try {
        // let user_id = await UserService.getUserID()
        let user_id = 1
        user_ID = user_id

        let response = await CourseService.searchCourseVoteInfo(
          user_ID,
          course_Name,
          coursecat_ID,
          status
        );
        this.interested_courses = response.data;
        return this.interested_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },

    async searchProposedInfo(user_ID, course_Name, coursecat_ID, status) {
      try {
        // const user_id = await UserService.getUserID()
        const user_id = 1
        user_ID = user_id

        let response = await CourseService.searchProposedInfo(
          user_ID,
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

    async searchCompletedInfo(user_ID, course_Name, coursecat_ID) {
      try {
        // const user_id = await UserService.getUserID()
        const user_id = 1
        user_ID = user_id

        let response = await CourseService.searchCompletedInfo(
          user_ID,
          course_Name,
          coursecat_ID,
        );
        this.completed_courses = response.data;
        return this.completed_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },

    async unvoteCourse(vote_Id) {
      try {
        // let user_id = await UserService.getUserID()
        let user_ID = 1

        let response = await CourseService.unvoteCourse(vote_Id, user_ID);
        console.log(response); 
        this.loadData();
      } catch (error) {
        console.error('Error unvoting course:', error);
      }
    },

    async loadData() {
      try {

        let registered_courses = await CourseService.searchCourseRegistrationInfo(this.user_ID, null, null, null)
        this.registered_courses = registered_courses.data

        let interested_courses = await CourseService.searchCourseVoteInfo(this.user_ID, null, null, null)
        this.interested_courses = interested_courses.data

        let proposed_courses = await CourseService.searchProposedInfo(this.user_ID, null, null, null)
        this.proposed_courses = proposed_courses.data

        let completed_courses = await CourseService.searchCompletedInfo(this.user_ID, null, null)
        this.completed_courses = completed_courses.data
        
      } catch (error) {
        console.error("Error fetching course details:", error);
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
      if (action == 'registered') {
        let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.registered_courses)
         if (sort_response.code == 200) {
          this.registered_courses = sort_response.data
         }
      }
      else if (action == 'interested') {
        let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.interested_courses)
         if (sort_response.code == 200) {
          this.interested_courses = sort_response.data
         }
      }
      else if (action == 'proposed') {
        let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.proposed_courses)
         if (sort_response.code == 200) {
          this.proposed_courses = sort_response.data
         }
      }
      else if (action == 'completed') {
        let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.completed_courses)
         if (sort_response.code == 200) {
          this.completed_courses = sort_response.data
         }
      }
    },
    isClosingDateValid(closingDate) {
        const regClosingDate = new Date(closingDate);
        return this.currentDate < regClosingDate;
    },
    editCourse(courseId) {
      this.$router.push({ name: 'editProposedCourse', params: { courseId } });
    }
  },
  computed: {
    displayedRegisteredCourses() {
      const startIndex = (this.localCurrentPageRegistered - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.registered_courses.slice(startIndex, endIndex);
    },
    displayedInterestedCourses() {
      const startIndex = (this.localCurrentPageInterested - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.interested_courses.slice(startIndex, endIndex);
    },
    displayedProposedCourses() {
      const startIndex = (this.localCurrentPageProposed - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.proposed_courses.slice(startIndex, endIndex);
    },
    displayedCompletedCourses() {
      const startIndex = (this.localCurrentPageCompleted - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.completed_courses.slice(startIndex, endIndex);
    }
  },
  async created() {
    try {

      let registered_response= await CourseService.searchCourseRegistrationInfo(this.user_ID, null, null, null)
      this.registered_courses = registered_response.data
      if (this.registered_courses == undefined || this.registered_courses.length == 0) {
        this.onInitialEmptyRegistered = true
      }

      let interested_response= await CourseService.searchCourseVoteInfo(this.user_ID, null, null, null)
      this.interested_courses = interested_response.data
      if (this.interested_courses == undefined || this.interested_courses.length == 0) {
        this.onInitialEmptyInterested = true
      }

      let proposed_response = await CourseService.searchProposedInfo(this.user_ID, null, null, null)
      this.proposed_courses = proposed_response.data
      if (this.proposed_courses == undefined || this.proposed_courses.length == 0) {
        this.onInitialEmptyProposed = true
      }

      let completed_response = await CourseService.searchCompletedInfo(this.user_ID, null, null, null)
      // console.log(completed_response.data)
      this.completed_courses = completed_response.data
      if (this.completed_courses == undefined || this.completed_courses.length == 0) {
        this.onInitialEmptyCompleted = true
      }
    } catch (error) {
      console.error("Error fetching course details:", error);
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