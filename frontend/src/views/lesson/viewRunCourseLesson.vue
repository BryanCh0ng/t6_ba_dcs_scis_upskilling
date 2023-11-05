<template>
  <div>
    <div class="container col-12 d-flex mb-3 w-100">
        <h5 v-if="lessons && lessons.length > 0" class="col m-auto">All Lessons for {{ lessons[0].run_Name }} </h5>
        <h5 v-else>All Lessons</h5>
        <button v-if="lessons && lessons.length > 0 && !isEndDatePassed(lessons[0].run_course.run_Enddate)" class="btn btn-primary" @click="goToCreateLesson(lessons.rcourse_ID)">Add Lesson</button>
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
              <th scope="col" class="actions">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(lesson, key) in displayedLessons" :key="key">
              <td>{{ lesson.instructor_Name }}</td>
              <td class="text-nowrap"><course-date-time :date="lesson.lesson_Date"></course-date-time></td>
              <td><course-date-time :time="lesson.lesson_Starttime"></course-date-time></td>
              <td><course-date-time :time="lesson.lesson_Endtime"></course-date-time></td>
              <td>{{ lesson.lesson_Status }}</td>
              <td v-if="lesson.lesson_Status=='Upcoming'" class="actions">
                <div class="action-buttons">
                  <course-action status="edit-lesson" @click="editLesson(lesson.lesson_ID)"></course-action>
                  <course-action status="remove-lesson" @click="removeLesson(lesson.lesson_ID)"></course-action>
                </div>
              </td>
              <td v-else></td>
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
import courseDateTime from "@/components/course/courseDateTime.vue";
import courseAction from '@/components/course/courseAction.vue';
import DefaultModal from "@/components/DefaultModal.vue";

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
    DefaultModal
  },
  data() {
    return {
      lessons: [],
      sortColumn: '',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 10,
      localCurrentPageLessons: 1,
      errorMsge: 'No records found',
      // Modal
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
        // console.log(response)
        if (response.code == 200) {
          this.lessons = response.lessons
        } else {
          this.errorMsge = response.message
        }
        // console.log(this.lessons)
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
    }
  },
  async created() {
    this.loadData();
  },
  
  }
</script>

<style>
@import '../../assets/css/paginate.css';

.action-buttons {
  display: flex;
  flex-wrap: nowrap;
  gap:10px;
}

th.actions, td.actions {
  width: 15%; 
}

</style>