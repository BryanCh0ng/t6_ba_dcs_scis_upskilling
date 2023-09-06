<template>
  <div>
    <ul class="nav nav-pills justify-content-center">
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

            <div class="container col-12 table-responsive">
            <h5 class="pb-3">Course(s) Assigned to Me</h5>
            <div v-if="assigned_courses && assigned_courses.length > 0">
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

            <div class="container col-12 table-responsive">
            <h5 class="pb-3">Course(s) Proposed by Me</h5>
            <div v-if="proposed_courses && proposed_courses.length > 0">
                <table class="table bg-white">
                <thead>
                    <tr class="text-nowrap">
                    <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('course_Name', 'proposed')">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                    <th scope="col">
                      <a href="" @click.prevent="sort('proposed_Date', 'proposed')" class="text-decoration-none text-dark">Propose Date <sort-icon :sortColumn="sortColumn === 'proposed_Date'" :sortDirection="getSortDirection('proposed_Date')"/></a></th>
                    <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('voteCount', 'proposed')"># of Interest <sort-icon :sortColumn="sortColumn === 'voteCount'" :sortDirection="getSortDirection('voteCount')"/></a></th>
                    <th scope="col">
                      <a href="" class="text-decoration-none text-dark" @click.prevent="sort('pcourse_Status', 'proposed')">Status <sort-icon :sortColumn="sortColumn === 'pcourse_Status'" :sortDirection="getSortDirection('pcourse_Status')"/></a></th>
                    <th scope="col">Reason</th>
                    <th scope="col">Course Details</th>
                    <th scope="col">Action(s)</th>
                    <th scope="col"></th>
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
                        <td class="status">{{ proposed_course.pcourse_Status }}</td>
                        <td class="reason">
                          {{ proposed_course.reason }}
                      </td>
                        <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(proposed_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                        <td v-if="proposed_course.pcourse_Status == 'Pending'">
                          <course-action status="Edit" :id="proposed_course.course_ID" @click="editCourse(proposed_course.course_ID)"></course-action>
                        </td>
                        <td v-else></td>
                        <td v-if="proposed_course.pcourse_Status == 'Pending'">
                          <course-action status="proposed_delete" :id="proposed_course.course_ID"></course-action>
                        </td>
                        <td v-else></td>
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

        <!-- Conducted -->
        <div class="tab-pane fade" :class="{ 'show active': activeTab === 'conducted' }">
            
            <student-search-filter
            :search-api="searchInstructorCompletedCourseInfo"
            @search-complete="handleSearchCompleteConducted" />

            <div class="container col-12 table-responsive">
            <h5 class="pb-3">Course(s) Taught by Me</h5>
            <div v-if="conducted_courses && conducted_courses.length > 0">
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
            <div v-else-if="conducted_courses=[]">
                <p>No records found</p>
            </div>
            </div>
            <vue-awesome-paginate v-if="conducted_courses.length/itemsPerPage > 0" v-model="localCurrentPageConducted" :totalItems="conducted_courses.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeConducted" class="justify-content-center pagination-container"/>
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
import courseNameDesc from '../../components/course/courseNameDesc.vue';
// import courseDateTime from '@/components/course/courseDateTime.vue';
import courseDate from '@/components/course/courseDate.vue';
import courseDuration from '@/components/course/courseDuration.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/CommonSearchFilter.vue";
import StudentSearchFilter from "@/components/search/StudentCourseSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";
// import UserService from "@/api/services/UserService.js";

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
    courseDuration
  },

  data() {
    return {
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
        statusOptionsAssigned: ["Enrolled", "Pending", "Not Enrolled", "Dropped"],
        statusOptionsProposed: ["Approved", "Rejected", "Pending"],
        currentDate: new Date(),
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
      try {
        // const user_id = await UserService.getUserID()
        const user_id = 4
        user_ID = user_id
        let response = await CourseService.searchInstructorAssignedCourseInfo(
          user_ID,
          course_Name,
          coursecat_ID,
          status
        );
        this.assigned_courses = response.data;
        console.log(this.assigned_courses)
        return this.assigned_courses;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
      }
    },

    async searchInstructorProposedCourseInfo(user_ID, course_Name, coursecat_ID, status) {
      try {
        // const user_id = await UserService.getUserID()
        const user_id = 4
        user_ID = user_id
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
      try {
        // const user_id = await UserService.getUserID()
        const user_id = 4
        user_ID = user_id
        let response = await CourseService.searchInstructorCompletedCourseInfo(
          user_ID,
          course_Name,
          coursecat_ID,
          status
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
          let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.assigned_courses)
          console.log(this.sortColumn)
          console.log(this.sortDirection)
          console.log(sort_response)
          if (sort_response.code == 200) {
            this.assigned_courses = sort_response.data
          }
        }

        if (action == 'proposed') {
          let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.proposed_courses)
          console.log(this.sortColumn)
          console.log(this.sortDirection)
          console.log(sort_response)
          if (sort_response.code == 200) {
            this.proposed_courses = sort_response.data
          }
        }

        if (action == 'conducted') {
          let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.conducted_courses)
          console.log(this.sortColumn)
          console.log(this.sortDirection)
          console.log(sort_response)
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
    try {
      // const user_ID = await UserService.getUserID()
      const user_ID = 4

      let assigned_courses = await CourseService.searchInstructorAssignedCourseInfo(user_ID, null, null, null)
      this.assigned_courses = assigned_courses.data
      console.log(this.assigned_coures)

      let proposed_courses = await CourseService.searchInstructorProposedCourseInfo(user_ID, null, null, null)
      this.proposed_courses = proposed_courses.data

      let conducted_courses = await CourseService.searchInstructorCompletedCourseInfo(user_ID, null, null)
      this.conducted_courses = conducted_courses.data

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