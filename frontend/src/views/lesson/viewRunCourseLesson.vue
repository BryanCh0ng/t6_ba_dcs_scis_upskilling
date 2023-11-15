<template>
  <div>
    <div class="container pt-5 col-12 d-flex mb-3 w-100">
        <h5 v-if="runcourse_Name" class="col m-auto">All Lessons for {{ runcourse_Name }} </h5>
        <h5 v-else>All Lessons</h5>
        <button v-if="userRole === 'Admin' && lessons && (lessons.length === 0 || (lessons.length > 0 && !isEndDatePassed(lessons[0].run_course.run_Enddate)))" class="btn btn-primary" @click="goToCreateLesson(lessons.rcourse_ID)">Add Lesson(s)</button>
    </div>

    <div class="container col-12 ">
      <div v-if="lessons && lessons.length > 0" class="table-responsive">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" @click.prevent="sort('instructor_Name')" class="text-decoration-none text-dark">Instructor Name <sort-icon :sortColumn="sortColumn === 'instructor_Name'" :sortDirection="getSortDirection('instructor_Name')"/></a>
              </th>
              <th scope="col">
                <a href="" @click.prevent="sort('lesson_Date')" class="text-decoration-none text-dark">Date <sort-icon :sortColumn="sortColumn === 'lesson_Date'" :sortDirection="getSortDirection('lesson_Date')"/></a></th>
              <th scope="col">Start Time</th>
              <th scope="col">End Time</th>
              <th scope="col">
                <a href="" @click.prevent="sort('lesson_Status')" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'lesson_Status'" :sortDirection="getSortDirection('lesson_Status')"/></a></th>
              <th scope="col" v-if="userRole != 'Student'">Attendance</th>
              <th scope="col" class="actions" v-if="userRole == 'Admin'">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(lesson, key) in displayedLessons" :key="key">
              <td>{{ lesson.instructor_Name }}</td>
              <td class="text-nowrap"><course-date-time :date="lesson.lesson_Date"></course-date-time></td>
              <td><course-date-time :time="lesson.lesson_Starttime"></course-date-time></td>
              <td><course-date-time :time="lesson.lesson_Endtime"></course-date-time></td>
              <td :class="{ 'text-grey-important': lesson.lesson_Status == 'Ended' }" ><course-status :status="lesson.lesson_Status"></course-status></td>
              <td v-if="userRole == 'Admin'" :class="{ 'text-grey-important': lesson.lesson_Status == 'Ended' }"><a class="text-nowrap text-dark text-decoration-underline view-runs" @click="goToViewAttendance(lesson.lesson_ID)">View Attendance</a></td>
              <td v-else-if="userRole == 'Trainer' && lesson.isTrainerForLesson" :class="{ 'text-grey-important': lesson.lesson_Status == 'Ended' }"><a class="text-nowrap text-dark text-decoration-underline view-runs" @click="goToViewAttendance(lesson.lesson_ID)">View Attendance</a></td>
              <td v-if="lesson.lesson_Status=='Upcoming' && userRole == 'Admin'" class="actions">
                <div class="action-buttons">
                  <course-action status="edit-lesson" @click="editLesson(lesson.lesson_ID)"></course-action>
                  <course-action status="remove-lesson" @click="removeLesson(lesson.lesson_ID)"></course-action>
                </div>
              </td>
              <td v-if="userRole === 'Admin'"></td>
            </tr>               
          </tbody>
        </table>
        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
        </div>

      </div>
      <div v-else-if="lessons=[]">
        <p>{{ errorMsge }}</p>
      </div>
    </div>
    <vue-awesome-paginate v-if="lessons.length/itemsPerPage > 0" v-model="localCurrentPageLessons" :totalItems="lessons.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeLessons" class="justify-content-center pagination-container"/>
    <DefaultModal :visible="showAlert" :title="title" :message="message" :variant="buttonType" @modal-closed="handleModalClosed" />
  </div>

</template>

<script>
import sortIcon from '@/components/common/sort-icon.vue';
import modalCourseContent from '@/components/course/modalCourseContent.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import CommonService from "@/api/services/CommonService.js";
import LessonService from "@/api/services/LessonService.js";
import UserService from "@/api/services/UserService.js";
import runCourseService from "@/api/services/runCourseService.js";
import courseDateTime from "@/components/course/courseDateTime.vue";
import courseAction from '@/components/course/courseAction.vue';
import DefaultModal from "@/components/DefaultModal.vue";
import courseStatus from '../../components/course/courseStatus.vue';

// Utility function to show a success message
function showSuccessMessage(vm) {
  vm.title = "Remove Lesson Successfully";
  vm.message = "You have successfully remove lesson for the run course.";
  vm.showAlert = true;
  vm.buttonType = "success";
}

// Utility function to show an unsuccessful message
function showUnsuccessMessage(vm) {
  vm.title = "Remove Lesson Unsucessful";
  vm.message = "Removal of the lesson from the course was unsuccessful.";
  vm.showAlert = true;
  vm.buttonType = "danger";
}
export default {
  components: {
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseDateTime,
    courseAction,
    DefaultModal,
    courseStatus,
  },
  data() {
    return {
      lessons: [],
      runcourse_Name: "",
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageLessons: 1,
      errorMsge: 'No records found',
      userRole: "",
      title: "",
      message: "",
      buttonType: "",
      showAlert: false,
    }
  },
  computed: {
    displayedLessons() {
      const startIndex = (this.localCurrentPageLessons - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.lessons.slice(startIndex, endIndex);
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
    handlePageChangeLessons(newPage) {
      this.localCurrentPageLessons = newPage;
      this.$emit('page-change', newPage);
    },
    async loadData() {
      try {
        const { id: course_ID } = this.$route.params;
        this.course_ID = course_ID
        
        let response = await LessonService.getRunCourseById(course_ID)
        if (response.code == 200) {
          this.lessons = response.lessons
        } else {
          this.errorMsge = response.message
        }
      } catch (error) {
        console.error("Error fetching lesson details:", error);
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
      let sort_response = await CommonService.sortRecords(this.sortColumn, this.sortDirection, this.lessons)
        if (sort_response.code == 200) {
          this.lessons = sort_response.data
        }
    },
    addEditLessons(courseID) {
      this.$router.push({ name: 'addEditLessons', params: {id: courseID}});
    }, 
    goToCreateLesson(courseID) {
        this.$router.push({ name: 'createRunCourseLesson', params: {id: courseID}});
    },
    editLesson(lessonId) {
      this.$router.push({ name: 'editRunCourseLesson', params: { id: lessonId }});
    },
    goToViewAttendance(lessonId) {
      this.$router.push({ name: 'viewAttendance', params: {lessonId: lessonId}});
    },
    isEndDatePassed(endDate) {
      const today = new Date();
      const runEndDate = new Date(endDate);
      return runEndDate < today;
    },
    async removeLesson(lesson_ID) {
      try {
        let response = await LessonService.removeLesson(lesson_ID);
        if (response.code == 200) {
          showSuccessMessage(this)
        } else {
          showUnsuccessMessage(this)
        }
        
      } catch (error) {
        showUnsuccessMessage(this)
        this.message = error.message;
      }
    },
    async handleModalClosed(value) {
      this.showAlert = value;
      this.loadData();   
    },
  },
  async created() {
    document.title = "Lessons | Upskilling Engagement System";
    const user_ID = await UserService.getUserID();
    const role = await UserService.getUserRole(user_ID);
    this.userRole = role;

    const runcourse_id = this.$route.params.id;
    const runcourse_info = await runCourseService.getRunCourseById(runcourse_id);
        
    if (runcourse_info) {
      this.runcourse_Name = runcourse_info.run_Name;
    }

    this.loadData()
  },
  
  }
</script>

<style>
@import '../../assets/css/course.css';
@import '../../assets/css/paginate.css';

</style>