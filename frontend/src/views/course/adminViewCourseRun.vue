<template>
  <div>

    <div class="container col-12 d-flex mb-3 w-100 pt-5">
      <h5 class="col m-auto">All Run Courses for '{{ course_Name }}'</h5>
      <button class="btn btn-primary" @click="goToCreateRunCourse(courses[0].course_ID)" title="Create Run Course">Create Run Course</button>
    </div>

        
    <div class="container col-12">
      <div v-if="courses && courses.length > 0" class="table-responsive">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" @click.prevent="sort('run_Name')" class="text-decoration-none text-dark">Run Name / Description <sort-icon :sortColumn="sortColumn === 'run_Name'" :sortDirection="getSortDirection('run_Name')"/></a></th>
              <th scope="col">
                <a href="" @click.prevent="sort('registration_count')" class="text-decoration-none text-dark">Registration Count <sort-icon :sortColumn="sortColumn === 'registration_count'" :sortDirection="getSortDirection('registration_count')"/></a></th>
              <th scope="col">
                <a href="" @click.prevent="sort('reg_Enddate')" class="text-decoration-none text-dark">Closing Date <sort-icon :sortColumn="sortColumn === 'reg_Enddate'" :sortDirection="getSortDirection('reg_Enddate')"/></a></th>
              <th scope="col">
                <a href="" @click.prevent="sort('runcourse_Status')" class="text-decoration-none text-dark">Run Status <sort-icon :sortColumn="sortColumn === 'runcourse_Status'" :sortDirection="getSortDirection('runcourse_Status')"/></a></th>
              <th scope="col">Course Details</th>
              <th scope="col">Lesson(s)</th>
              <th scope="col">Registration(s)</th>
              <th scope="col">Feedback</th>
              <th scope="col">Feedback Template</th>
              <th scope="col">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, key) in displayedCourses" :key="key">
              <td class="name">
                <course-name-desc :name="course.run_Name" :category="course.coursecat_Name" :description="course.course_Desc"></course-name-desc>
              </td>
              <td class="reg_count">
                {{ course.registration_count }}
              </td>
              <td class="closing_date">
                <course-date-time :date="course.reg_Enddate" :time="course.reg_Endtime"></course-date-time>
              </td>
              <td class="pl-0 border-top">
                <course-status :status="course.runcourse_Status"></course-status>
              </td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-lessons" @click="viewLessons(course.rcourse_ID)">View Lessons</a></td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-registrations" @click="viewRegistrations(course.rcourse_ID)">View Registrations</a></td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis" @click="goToRunCourseFeedbackAnalysis(course.rcourse_ID)">View Feedback Analysis</a></td>
              <td v-if="course.feedback_Startdate && isBeforeCurrentDate(course.feedback_Startdate)"><a v-if="course.course_Status != 'Retired'" class="btn bg-light-blue" @click="openFeedbackTemplateModal(course)" data-bs-toggle="modal" data-bs-target="#apply_course_feedback_template_modal">Apply Feedback Template</a></td>
              <td v-else><a v-if="course.course_Status != 'Retired'" class="btn bg-light-blue disabled" title="Unable to remove run course due to ongoing/past feedback period'">Apply Feedback Template</a></td>
              <td v-if="course.runcourse_Status=='Ongoing'">
                <course-action @action-and-message-updated="handleActionData" status="close_registration" :course="course" :courseName="course.courseName" ></course-action>
              </td>
              <td v-else-if="course.runcourse_Status=='Closed'">
                <course-action @action-and-message-updated="handleActionData" status="open_for_registration" :course="course" :courseName="course.courseName" ></course-action>
              </td>
              <td><course-action status="add-edit-lessons"></course-action></td>
              <td><course-action status="Edit" :course="course" @click="goToEditRunCourseWithId(course.rcourse_ID)"></course-action></td>
              <td v-if="course.runcourse_Status=='Closed' && isBeforeRunCourseDate(course.reg_Startdate)">
                <course-action @action-and-message-updated="handleActionData" status="delete-run-course" :course="course" :courseName="course.courseName" ></course-action>
              </td>
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

      <div class="modal fade" id="apply_course_feedback_template_modal" tabindex="-1" aria-hidden="true" ref="applyCourseFeedbackTemplateModal">
      <div class="modal-dialog modal-lg"> 
        <course-apply-feedback-template-modal :modalOpen="modalOpenFeedbackTemplate" v-if="showFeedbackTemplateModal" @model-after-action-close="modalAfterActionClose" :course="selectedCourse" @close-modal="closeFeedbackTemplateModal" />
      </div>
    </div>
  
    </div>
  
  </template>
    
  <script>

  import courseAction from '@/components/course/courseAction.vue';
  import sortIcon from '@/components/common/sort-icon.vue';
  import modalCourseContent from '@/components/course/modalCourseContent.vue';
  import courseNameDesc from '@/components/course/courseNameDesc.vue';
  import courseDateTime from '@/components/course/courseDateTime.vue';
  import { VueAwesomePaginate } from 'vue-awesome-paginate';
  import CourseService from "@/api/services/CourseService.js";
  import modalAfterAction from '@/components/course/modalAfterAction.vue';
  import courseApplyFeedbackTemplateModal from '@/components/course/courseApplyFeedbackTemplateModal.vue';
  import CommonService from "@/api/services/CommonService.js";
  import courseStatus from '@/components/course/courseStatus.vue';
  
  export default {
    components: {
      courseAction,
      sortIcon,
      modalCourseContent,
      VueAwesomePaginate,
      courseNameDesc,
      courseDateTime,
      modalAfterAction,
      courseApplyFeedbackTemplateModal,
      courseStatus
    },
    data() {
      return {
        courses: [],
        sortColumn: '',
        sortDirection: 'asc',
        selectedCourse: null,
        itemsPerPage: 10,
        localCurrentPageCourses: 1,
        statusOptions: ["Ongoing", "Closed"],
        receivedMessage: '',
        actionCourse: {},
        search_status: null,
        search_course_name: null,
        search_course_category: null,
        modalOpenFeedbackTemplate: false,
        showFeedbackTemplateModal: false,
        course_Name: '',
        course_ID: '',
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
      handleActionData(actionData) {
        this.receivedMessage = actionData.message;
        this.actionCourse = actionData.course
        const modalButtonElement = this.$el.querySelector('.invisible-btn')
        modalButtonElement.click();
      },
      async loadData() {
        try {
          const course_id = this.$route.params.id
          let response = await CourseService.searchAllRunCourseByCourseId(this.search_course_name, this.search_course_category, this.search_status, course_id)
          this.courses = response.data
        } catch (error) {
          console.error("Error fetching course details:", error);
        }
      },
      modalAfterActionClose() {
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
      goToEditRunCourseWithId(runcourseID) {
        this.$router.push({ name: 'editRunCourse', params: {id: runcourseID}})
      },
      goToCreateRunCourse(courseID){
        this.$router.push({ name: 'createRunCourse', params: {id: courseID}});
      },
      openFeedbackTemplateModal(course) {
        this.selectedCourse = course
        this.modalOpenFeedbackTemplate = !this.modalOpenFeedbackTemplate;
        this.showFeedbackTemplateModal = true;
      },
      closeFeedbackTemplateModal() {
        this.modalOpenFeedbackTemplate = false;
        this.showFeedbackTemplateModal = false;
        this.selectedCourse = null;
      },
      isCourseStartDateBeforeCurrentDate(courseStartDate) {
        console.log(courseStartDate)
        const currentDate = new Date();
        return new Date(courseStartDate) > currentDate;
      },
      isBeforeCurrentDate(feedbackStartDate){
        const currentDate = new Date();
        return new Date(feedbackStartDate) > currentDate;
      },
      goToRunCourseFeedbackAnalysis(courseID) {
        this.$router.push({ name: 'viewRunCourseFeedbackAnalysis', params: {id: courseID}});
      },
      isBeforeRunCourseDate(runRegStartDate){
        const currentDate = new Date();
        return new Date(runRegStartDate) > currentDate;
      },
      viewLessons(courseID) {
        this.$router.push({ name: 'viewRunCourseLesson', params: {id: courseID}});
      },
      viewRegistrations(runcourseID) {
        this.$router.push({ name: 'adminViewRegistration', params: {id: runcourseID}});
      },
      addEditLessons(courseID) {
        this.$router.push({ name: 'addEditLessons', params: {id: courseID}});
      }
    },
    async created() {
      document.title = "Run Courses | Upskilling Engagement System";

      const { id: course_ID } = this.$route.params;
      this.course_ID = course_ID

      let response = await CourseService.getCourseName(this.course_ID);
      this.course_Name = response.data
      this.loadData();
    },
    mounted() {
      const buttonElement = document.createElement('button');
      buttonElement.className = 'btn btn-primary d-none invisible-btn';
      buttonElement.setAttribute('data-bs-toggle', 'modal');
      buttonElement.setAttribute('data-bs-target', '#after_action_modal');
      this.$el.appendChild(buttonElement);
      const modalElement = this.$refs.afterActionModal;
      modalElement.addEventListener('hidden.bs.modal', this.modalAfterActionClose);

      const buttonElement2 = document.createElement('button');
      buttonElement2.className = 'btn btn-primary d-none invisible-btn';
      buttonElement2.setAttribute('data-bs-toggle', 'modal');
      buttonElement2.setAttribute('data-bs-target', '#apply_course_feedback_template_modal'); 
      this.$el.appendChild(buttonElement2);
      const modalElement2 = this.$refs.applyCourseFeedbackTemplateModal;
      modalElement2.addEventListener('hidden.bs.modal', this.modalAfterActionClose);
    },
    beforeUnmount() {
      const modalElement = this.$refs.afterActionModal;
      modalElement.removeEventListener('hidden.bs.modal', this.modalAfterActionClose);

      const modalElement2 = this.$refs.applyCourseFeedbackTemplateModal;
      modalElement2.removeEventListener('hidden.bs.modal', this.modalAfterActionClose)
    },
    }
  </script>
  
  <style>
    @import '../../assets/css/course.css';
    @import '../../assets/css/paginate.css';
  </style>