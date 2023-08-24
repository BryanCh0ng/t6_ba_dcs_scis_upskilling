<template>
  <div>
    <div class="pt-5 container col-12 table-responsive">
      <h5 class="pb-3">Courses Available for Students to Indicate Interest</h5>
      <div v-if="vote_courses.length > 0">
        <table class="table">
          <thead>
            <tr class="text-nowrap">
            <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
            <th scope="col">
                <a href="" class="text-decoration-none text-dark"># of Current Interest <sort-icon :sortColumn="sortColumn === 'reg_count'" :sortDirection="sortDirection"/></a></th>
            <th scope="col">
                <a href="" class="text-decoration-none text-dark">Status <sort-icon :sortColumn="sortColumn === 'status'" :sortDirection="sortDirection"/></a></th>
            <th scope="col">Course Details</th>
            <th scope="col">Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(vote_course, key) in displayedVoteCourses" :key="key">
            <td class="name">
              <course-name-desc :name="vote_course.name" :category="vote_course.category" :description="vote_course.description"></course-name-desc>
            </td>
            <td class="current_interest">
                {{ vote_course.interest_count }}
            </td>
            <td>{{ vote_course.status }}</td>
            <td><a class="text-nowrap text-dark text-decoration-underline view-course-details"  @click="openModal(vote_course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">View Course Details</a></td>
            <td v-if="vote_course.status === 'Open'"><course-action status="Close" :id="vote_course.id"></course-action></td>
            <td v-else-if="vote_course.status === 'Closed'"><course-action status="Open for Registration" :id="vote_course.id"></course-action></td>
            </tr>
          </tbody>
        </table>
        <div class="modal fade" id="course_details_modal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg"><modal-course-content v-if="selectedCourse" :course="selectedCourse" @close-modal="closeModal" /></div>
        </div>
      </div>
      <div v-else>
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-model="localCurrentPage" :totalItems="vote_courses.length" :items-per-page="1" @page-change="handlePageChange" class="justify-content-center pagination-container"/>
  </div>
</template>
    
<script>
import courseAction from '../../components/course/courseAction.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import courseNameDesc from '../../components/course/courseNameDesc.vue';

export default {
  components: {
    courseAction,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate,
    courseNameDesc
  },
  data() {
    return {
      vote_courses: [
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
        status: 'Open',
        interest_count: 13
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
        status: 'Close',
        interest_count: 20
        },
      ],
      sortColumn: 'name',
      sortDirection: 'asc',
      selectedCourse: null,
      itemsPerPage: 1,
      localCurrentPage: 1,
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
  },
  computed: {
    displayedVoteCourses() {
      const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.vote_courses.slice(startIndex, endIndex);
    },
  }
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>