<template>
    <div>
      <search-filter
        :status-options="statusOptions"
        :search-api="searchAllCourseAdmin" 
        @search-complete="handleSearchComplete" 
        :default-status="'Active'" />

      <div class="container col-12 d-flex mb-3 w-100">
          <h5 class="col m-auto">All Courses</h5>
          <button class="btn btn-primary" @click="goToCreateCourse" title="Create Course">Create Course</button>
      </div>

      <div class="container col-12">
        <div v-if="courses && courses.length > 0" class="table-responsive">
          <table class="table bg-white">
            <thead>
              <tr class="text-nowrap">
                <th scope="col">
                  <a href="" @click.prevent="sort('course_Name')" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'course_Name'" :sortDirection="getSortDirection('course_Name')"/></a></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('course_Status')" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'course_Status'" :sortDirection="getSortDirection('course_Status')"/></a></th>
                <th scope="col">Feedback</th>
                <th scope="col">Course Details</th>
                <th scope="col">Course Run(s)</th>
                <th scope="col">Action(s)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(course, key) in displayedCourses" :key="key">
                <td class="name">
                  <course-name-desc :name="course.course_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
                </td>
                <td>{{ course.course_Status }}</td>
                <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis" @click="goToViewCourseFeedback(course.course_ID)">View Feedback</a></td>
                <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
                <td><a class="text-nowrap text-dark text-decoration-underline view-runs" @click="goToViewCourseRun(course.course_ID)">View Runs</a></td>
                <div>
                  <td v-if="course.course_Status === 'Active'"><course-action status="Deactivate" @action-and-message-updated="handleActionData" :course="course"></course-action></td>
                  <td v-else-if="course.course_Status === 'Inactive'"><course-action status="Activate" @action-and-message-updated="handleActionData" :course="course"></course-action></td>
                  <td v-if="course.course_Status != 'Retired'"><course-action status="Edit" :course="course" @click="goToEditCourseWithId(course.course_ID)"></course-action></td>
                  <td v-if="course.course_Status === 'Active'"><course-action status="create_run" :course="course" @click="goToCreateRunCourseWithId(course.course_ID)"></course-action></td>
                  <td v-else-if="course.course_Status === 'Inactive'"><course-action status="Retire" @action-and-message-updated="handleActionData" :course="course"></course-action></td>
                </div>
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
      
      <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
        <div class="modal-dialog modal-lg"> 
          <modal-after-action :course="actionCourse" @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal" />
        </div>
      </div>

    </div>
  
</template>
  
<script>
  import courseAction from '@/components/course/courseAction.vue';
  import sortIcon from '@/components/common/sort-icon.vue';
  import modalCourseContent from '@/components/course/modalCourseContent.vue';
  import courseNameDesc from '@/components/course/courseNameDesc.vue';
  import { VueAwesomePaginate } from 'vue-awesome-paginate';
  import SearchFilter from "@/components/search/AdminCommonSearchFilter.vue";
  import CourseService from "@/api/services/CourseService.js";
  import modalAfterAction from '@/components/course/modalAfterAction.vue';
  import CommonService from "@/api/services/CommonService.js";
  import UserService from "@/api/services/UserService.js";
  
  export default {
    components: {
      courseAction,
      sortIcon,
      modalCourseContent,
      VueAwesomePaginate,
      courseNameDesc,
      SearchFilter,
      modalAfterAction
    },
    data() {
      return {
        courses: [],
        sortColumn: '',
        sortDirection: 'asc',
        selectedCourse: null,
        itemsPerPage: 10,
        localCurrentPageCourses: 1,
        statusOptions: ["Active", "Inactive", "Retired"],
        receivedMessage: '',
        actionCourse: {},
        search_status: 'Active',
        search_course_name: null,
        search_course_category: null,
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
        // console.log("searchResults", searchResults);
        this.courses = searchResults;
        
      },
      async searchAllCourseAdmin(courseName, coursecat_ID, status) {
        this.search_course_name = courseName
        this.search_course_category = coursecat_ID
        this.search_status = status
        try {
          let response = await CourseService.searchAllCourseAdmin(courseName, coursecat_ID, status);
          this.courses = response.data;
          
          return this.courses;
        } catch (error) {
          console.error("Error fetching info:", error);
          throw error;
        }
      },
      handleActionData(actionData) {
        this.receivedMessage = actionData.message;
        this.actionCourse = actionData.course
        const modalButtonElement = this.$el.querySelector('.invisible-btn')
        modalButtonElement.click();
      },
      async loadData() {
        console.log('load')
        try {
          let response = await CourseService.searchAllCourseAdmin(this.search_course_name, this.search_course_category, this.search_status)
          
          this.courses = response.data
          // console.log(this.courses)
        } catch (error) {
          console.error("Error fetching course details:", error);
        }
      },
      modalAfterActionClose() {
        console.log('test')
        this.loadData();
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
        let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.courses)
          if (sort_response.code == 200) {
            this.courses = sort_response.data
          }
      },
      goToEditCourseWithId(courseID) {
        this.$router.push({ name: 'editCourse', params: {id: courseID}})
      },
      goToCreateRunCourseWithId(courseID){
        this.$router.push({ name: 'createRunCourse', params: {id: courseID}});
      },
      goToCreateCourse() {
        this.$router.push({ name: 'createCourse'});
      },
      goToViewCourseRun(courseID) {
        this.$router.push({ name: 'adminViewCourseRun', params: {id: courseID}});
      },
      goToViewCourseFeedback(course_ID) {
        this.$router.push({ name: 'viewCourseFeedback', params: { id: course_ID } });
      }
    },
    async created() {
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
      buttonElement.setAttribute('data-bs-target', '#after_action_modal');
      this.$el.appendChild(buttonElement);
      const modalElement = this.$refs.afterActionModal;
      modalElement.addEventListener('hidden.bs.modal', this.modalAfterActionClose);
    },
    beforeUnmount() {
      const modalElement = this.$refs.afterActionModal;
      modalElement.removeEventListener('hidden.bs.modal', this.modalAfterActionClose)
    },
    }
</script>
  
  <style>
    @import '../../assets/css/course.css';
    @import '../../assets/css/paginate.css';
  </style>