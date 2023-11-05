<template>
  <div>
    <ul class="nav nav-pills justify-content-center pt-4">
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'assigned' }" @click="activeTab = 'assigned'">Assigned</a>
      </li> 
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'proposed' }" @click="activeTab = 'proposed'">Proposed</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ 'active': activeTab === 'conducted' }" @click="activeTab = 'conducted'">Conducted</a>
      </li> 
    </ul>
    <div class="tab-content ">
        <!-- Assigned -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'assigned' }">
            <student-search-filter
            :search-api="searchInstructorAssignedCourseInfo"
            @search-complete="handleSearchCompleteAssigned" />

            <div class="container col-12">
            <h5 class="pb-3">Course(s) Assigned to Me</h5>
            <div v-if="assigned_courses && assigned_courses.length > 0" class="table-responsive">
                <table class="table bg-white">
                <thead>
                    <tr class="text-nowrap">
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'assigned')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                    <th scope="col">Venue</th>
                     <th scope="col">
                        <a href="" @click.prevent="sort('run_Startdate', 'assigned')" class="text-decoration-none text-dark">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                     <th scope="col">
                        <a href="" @click.prevent="sort('run_Enddate', 'assigned')" class="text-decoration-none text-dark">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                    <th scope="col">Start & End Time</th>
                    <th scope="col">Course Details</th>
                    <th scope="col">Action(s)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(assigned_course, key) in displayedAssignedCourses" :key="key">
                        <td class="name">
                            <course-name-desc :name="assigned_course.course_Name" :category="assigned_course.coursecat_Name" :description="assigned_course.course_Desc"></course-name-desc>
                        </td>
                        <td> {{ assigned_course.course_Venue }} </td>
                        <td class="start_date">
                            <course-date :date="assigned_course.run_Startdate"></course-date>
                        </td>
                        <td class="end_date">
                            <course-date :date="assigned_course.run_Enddate"></course-date>
                        </td>
                        <td class="time">
                          <course-duration :start_time="assigned_course.run_Starttime" :end_time="assigned_course.run_Endtime"></course-duration> 
                        </td>
                        <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(assigned_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                        <td>
                          <course-action status="attendance" :id="assigned_course.course_ID"></course-action>
                        </td>
                    </tr>
                </tbody>
                </table>
            </div>
            <div v-else-if="assigned_courses=[] && onInitialEmptyAssigned">
              <div class="pt-5 text-center">
                <p>You are not assigned to any courses.</p>
                <router-link :to="{ name: 'proposeCourse' }" class="btn btn-edit">Propose a Course</router-link>
              </div>
            </div>
            <div v-else-if="assigned_courses=[]">
                <p>No records found</p>
            </div>
            </div>
            <vue-awesome-paginate v-if="assigned_courses.length/itemsPerPage > 0" v-model="localCurrentPageAssigned" :totalItems="assigned_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeAssigned" class="justify-content-center pagination-container"/>
        </div>

        <!-- Proposed -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'proposed' }">
            <search-filter
            :status-options="statusOptionsProposed"
            :search-api="searchInstructorProposedCourseInfo"
            @search-complete="handleSearchCompleteProposed" />

            <div class="container col-12">
            <h5 class="pb-3">Course(s) Proposed by Me</h5>
            <div v-if="proposed_courses && proposed_courses.length > 0" class="table-responsive">
                <table class="table bg-white">
                <thead>
                    <tr class="text-nowrap">
                    <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'proposed')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                    <th scope="col">
                      <a href="" @click.prevent="sort('proposed_Date', 'proposed')" class="text-decoration-none text-dark">Proposed Date <sort-icon :sortColumn="sortColumn === 'proposed_Date'" :sortDirection="getSortDirection('proposed_Date')"/></a></th>
                    <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('voteCount', 'proposed')"># of Interest <sort-icon :sortColumn="sortColumn === 'voteCount'" :sortDirection="getSortDirection('voteCount')"/></a></th>
                    <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('pcourse_Status', 'proposed')">Status <sort-icon :sortColumn="sortColumn === 'pcourse_Status'" :sortDirection="getSortDirection('pcourse_Status')"/></a></th>
                    <th scope="col">Course Details</th>
                    <th scope="col">Action(s)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(proposed_course, key) in displayedProposedCourses" :key="key">
                        <td class="name">
                            <course-name-desc :name="proposed_course.course_Name" :category="proposed_course.coursecat_Name" :description="proposed_course.course_Desc"></course-name-desc>
                        </td>
                        <td class="proposed_date">
                          <course-date :date="proposed_course.proposed_Date"></course-date>
                        </td>
                        <td class="vote_count">{{ proposed_course.voteCount }}</td>
                        <td class="pl-0 border-top">
                          <course-status :status="proposed_course.pcourse_Status"></course-status>
                        </td>
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
            <div v-else-if="proposed_course=[] && onInitialEmptyProposed">
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

        <!-- Conducted -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'conducted' }">
            
            <student-search-filter
            :search-api="searchInstructorCompletedCourseInfo"
            @search-complete="handleSearchCompleteConducted" />

            <div class="container col-12">
            <h5 class="pb-3">Course(s) Taught by Me</h5>
            <div v-if="conducted_courses && conducted_courses.length > 0" class="table-responsive">
                <table class="table bg-white">
                <thead>
                    <tr class="text-nowrap">
                    <th scope="col">
                        <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'conducted')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                    <th scope="col">
                      <a href="" @click.prevent="sort('course_Venue', 'conducted')" class="text-decoration-none text-dark">Venue <sort-icon :sortColumn="sortColumn === 'course_Venue'" :sortDirection="getSortDirection('course_Venue')"/></a></th>
                    <th scope="col">
                      <a href="" @click.prevent="sort('run_Startdate', 'conducted')" class="text-decoration-none text-dark">Course Start Date <sort-icon :sortColumn="sortColumn === 'run_Startdate'" :sortDirection="getSortDirection('run_Startdate')"/></a></th>
                    <th scope="col">
                      <a href="" @click.prevent="sort('run_Enddate', 'conducted')" class="text-decoration-none text-dark">Course End Date <sort-icon :sortColumn="sortColumn === 'run_Enddate'" :sortDirection="getSortDirection('run_Enddate')"/></a></th>
                    <th scope="col">Course Details</th>
                    <th scope="col">Action(s)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(conducted_course, key) in displayedConductedCourses" :key="key">
                    <td class="name">
                        <course-name-desc :name="conducted_course.course_Name" :category="conducted_course.coursecat_Name" :description="conducted_course.course_Desc"></course-name-desc>
                    </td>
                    <td> {{ conducted_course.course_Venue }} </td>
                    <td class="start_date">
                        <course-date :date="conducted_course.run_Startdate"></course-date>
                    </td>
                    <td class="end_date">
                        <course-date :date="conducted_course.run_Enddate"></course-date>
                    </td>
                    <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(conducted_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                    <td>
                      <course-action status="feedback-analysis" :id="conducted_course.course_ID"></course-action>
                    </td>
                    </tr>
                </tbody>
                </table>
               
            </div>
            <div v-else-if="conducted_courses=[] && onInitialEmptyConducted">
              <div class="pt-5 text-center">
                <p>You have not yet conducted any courses.</p>
                <router-link :to="{ name: 'proposeCourse' }" class="btn btn-edit">Propose a Course</router-link>
              </div>
            </div>
            <div v-else-if="conducted_courses=[]">
                <p>No records found</p>
            </div>
            </div>
            <vue-awesome-paginate v-if="conducted_courses.length/itemsPerPage > 0" v-model="localCurrentPageConducted" :totalItems="conducted_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeConducted" class="justify-content-center pagination-container"/>
        </div>

        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
        </div>

        <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
            <div class="modal-dialog modal-lg"> 
              <modal-after-action :course="actionCourse" @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal" />
            </div>
          </div>
          
        <div class="modal fade" id="rejected_course_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <modal-after-action
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
import courseDate from '@/components/course/courseDate.vue';
import courseDuration from '@/components/course/courseDuration.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/CommonSearchFilter.vue";
import StudentSearchFilter from "@/components/search/StudentCourseSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";
import UserService from "@/api/services/UserService.js";
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
    StudentSearchFilter,
    courseDate,
    courseDuration,
    modalAfterAction,
    courseStatus
  },

  data() {
    return {
        user_ID:null,
        assigned_courses: [],
        proposed_courses: [],
        conducted_courses: [],
        sortColumn: '',
        sortDirection: 'asc',
        selectedCourse: null,
        itemsPerPage: 10,
        localCurrentPageAssigned: 1,
        localCurrentPageProposed: 1,
        localCurrentPageConducted: 1,
        activeTab: 'assigned',
        statusOptionsProposed: ["Approved", "Rejected", "Pending"],
        currentDate: new Date(),
        receivedMessage: '',
        actionCourse: {},
        showRejectedCourseModal: false,
        selectedRejectedCourse: null,
        receivedRejectedCourseMessage: '',
        onInitialEmptyAssigned: false,
        onInitialEmptyProposed: false,
        onInitialEmptyConducted: false,
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
    handleActionData(actionData) {
      // console.log(actionData.message)
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

    handlePageChangeAssigned(newPage) {
      this.localCurrentPageAssigned = newPage;
      this.$emit('page-change', newPage);
    },

    handlePageChangeProposed(newPage) {
      this.localCurrentPageProposed = newPage;
      this.$emit('page-change', newPage);
    },

    handlePageChangeConducted(newPage) {
      this.localCurrentPageConducted = newPage;
      this.$emit('page-change', newPage);
    },

    async handleSearchCompleteAssigned(searchResults) {
      // console.log(searchResults)
      this.assigned_courses = searchResults;
    },

    async handleSearchCompleteProposed(searchResults) {
      // console.log(searchResults)
      this.proposed_courses = searchResults;
    },

    async handleSearchCompleteConducted(searchResults) {
      // console.log(searchResults)
      this.conducted_courses = searchResults;
    },

    async searchInstructorAssignedCourseInfo(user_ID, course_Name, coursecat_ID, status) {
      const user_id = await UserService.getUserID();
      user_ID = user_id
      try {
      let response = await CourseService.searchInstructorAssignedCourseInfo(
          user_ID,
          course_Name,
          coursecat_ID,
          status
        );
        this.assigned_courses = response.data;
        // console.log(this.assigned_courses)
        return this.assigned_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },

    async searchInstructorProposedCourseInfo(user_ID, course_Name, coursecat_ID, status) {
      const user_id = await UserService.getUserID();
      user_ID = user_id
      try {
        let response = await CourseService.searchInstructorProposedCourseInfo(
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

    async searchInstructorCompletedCourseInfo(user_ID, course_Name, coursecat_ID) {
      const user_id = await UserService.getUserID();
      user_ID = user_id
      try {
        let response = await CourseService.searchInstructorCompletedCourseInfo(
          user_ID,
          course_Name,
          coursecat_ID
        );
        this.conducted_courses = response.data;
        return this.conducted_courses;
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
        if (action == 'assigned') {
          let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.assigned_courses)
          if (sort_response.code == 200) {
            this.assigned_courses = sort_response.data
          }
        }

        if (action == 'proposed') {
          let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.proposed_courses)
         
          if (sort_response.code == 200) {
            this.proposed_courses = sort_response.data
          }
        }

        if (action == 'conducted') {
          let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.conducted_courses)
          
          if (sort_response.code == 200) {
            this.conducted_courses = sort_response.data
          }
        }
    },
    isClosingDateValid(closingDate) {
        const regClosingDate = new Date(closingDate);
        return this.currentDate < regClosingDate;
    },

    editCourse(courseId) {
      this.$router.push({ name: 'editProposedCourse', params: { courseId } });
    },

    async loadData() {
      try {
          const user_ID = await UserService.getUserID();
          console.log(user_ID)
          
          let assigned_courses = await CourseService.searchInstructorAssignedCourseInfo(user_ID, null, null, null)
          this.assigned_courses = assigned_courses.data

          let proposed_courses = await CourseService.searchInstructorProposedCourseInfo(user_ID, null, null, null)
          this.proposed_courses = proposed_courses.data

          let conducted_courses = await CourseService.searchInstructorCompletedCourseInfo(user_ID, null, null)
          this.conducted_courses = conducted_courses.data
        
      } catch (error) {
        console.error("Error fetching course details:", error);
      }
    },

    async getUserID() {
      try {
        const user_ID = await UserService.getUserID();
        this.user_ID = user_ID;
      } catch (error) {
        console.error('Error fetching user ID:', error);
        this.user_ID = null;
      }
    },

  },
  computed: {
    displayedAssignedCourses() {
      const startIndex = (this.localCurrentPageAssigned - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.assigned_courses.slice(startIndex, endIndex);
    },

    displayedProposedCourses() {
      const startIndex = (this.localCurrentPageProposed - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.proposed_courses.slice(startIndex, endIndex);
    },

    displayedConductedCourses() {
      const startIndex = (this.localCurrentPageConducted - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.conducted_courses.slice(startIndex, endIndex);
    },

  },
  async created() {
    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);
    if (role == 'Student') {
      this.$router.push({ name: 'studentViewProfile' }); 
    } else if (role == 'Admin') {
      this.$router.push({ name: 'AdminViewInstructorsTrainers' }); 
    } else {
      try {
        this.user_ID = await UserService.getUserID()

        let assigned_courses = await CourseService.searchInstructorAssignedCourseInfo(this.user_ID, null, null, null)
        if (assigned_courses.code == 200) {
          this.assigned_courses = assigned_courses.data
          if (this.assigned_courses == undefined || this.assigned_courses.length == 0) {
            this.onInitialEmptyAssigned = true
          }
        } else {
          this.assigned_courses = []
          this.onInitialEmptyAssigned = true
        }

        console.log(this.user_ID)

        let proposed_courses = await CourseService.searchInstructorProposedCourseInfo(this.user_ID, null, null, null)
        if (proposed_courses.code == 200 ) {
          this.proposed_courses = proposed_courses.data
          if (this.proposed_courses == undefined || this.proposed_courses.length == 0) {
            this.onInitialEmptyProposed = true
          }
        } else {
          this.proposed_courses = []
          this.onInitialEmptyProposed = true
        }

        let conducted_courses = await CourseService.searchInstructorCompletedCourseInfo(this.user_ID, null, null)
        if (conducted_courses.code == 200) {
          this.conducted_courses = conducted_courses.data
          if (this.conducted_courses == undefined || this.conducted_courses.length == 0) {
            this.onInitialEmptyConducted = true
          }
        } else {
          this.conducted_courses = []
          this.onInitialEmptyConducted = true
        }
        
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