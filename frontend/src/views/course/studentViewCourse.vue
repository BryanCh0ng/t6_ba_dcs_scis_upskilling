<template>
  <div>
    <div class="pt-5 container col-12 table-responsive">
      <h5 class="pb-3">All Courses</h5>

      <div v-if="courses.length > 0">
        <table class="table">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon ::sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course Start Date <sort-icon :sortColumn="sortColumn === 'start_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course End Date <sort-icon :sortColumn="sortColumn === 'end_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">Course Details</th>
              <th scope="col">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, key) in displayedCourses" :key="key">
              <td class="name">
                <course-name-desc :name="course.name" :category="course.category" :description="course.description"></course-name-desc>
              </td>
              <td class="start_date">
                <course-date :date="course.start_date" :time="course.start_time"></course-date>
              </td>
              <td class="end_date">
                <course-date :date="course.end_date" :time="course.end_time"></course-date>
              </td>
              <td class="closing_date">
                <course-date :date="course.closing_date" :time="course.closing_time"></course-date>
              </td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
              <td><course-action :status="course.status" :id="course.id"></course-action></td>
            </tr>
          </tbody>
        </table>

        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" />
          </div>
        </div>
      </div>

      <div v-else>
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-if="courses.length/itemsPerPage > 0" v-model="localCurrentPage" :totalItems="courses.length" :items-per-page="1" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
  </div>
</template>

<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import courseNameDesc from '../../components/course/courseNameDesc.vue';
import courseDate from '../../components/course/courseDate.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    courseNameDesc,
    VueAwesomePaginate,
    courseDate
  },
  data() {
    return {
      courses: [
        {
          id: 1,
          name: "Course Name 1",
          category: "SCIS",
          description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
          start_date: "Aug 20, 2023",
          start_time: "6.30 pm",
          end_date: "Aug 20, 2023",
          end_time: "6.30 pm",
          closing_date: "Aug 20, 2023",
          closing_time: "6.30 pm",
          fee: 50,
          venue: 'SCIS SR-2',
          format: 'Physical',
          status: 'Active',
          available_slots: 13
        },
        {
          id: 2,
          name: "Course Name 2",
          category: "LKCSB",
          description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore",
          start_date: "Aug 20, 2023",
          start_time: "6.30 pm",
          end_date: "Aug 20, 2023",
          end_time: "6.30 pm",
          closing_date: "Aug 20, 2023",
          closing_time: "6.30 pm",
          fee: 100,
          venue: 'SCIS SR-5',
          format: 'Online',
          status: 'Vote',
          available_slots: 15
        },
      ],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 1,
      localCurrentPage: 1,
    }
  },
  computed: {
    displayedCourses() {
      const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
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
    handlePageChange(newPage) {
      this.localCurrentPage = newPage;
      this.$emit('page-change', newPage);
    }
  }
};
</script>

<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>