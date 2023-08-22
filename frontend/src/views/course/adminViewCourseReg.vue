<template>
  <div>

      <div class="pt-5 container col-12 table-responsive">
      <h5 class="pb-3">All Courses Available for Registration</h5>

      <div v-if="courses.length > 0">
          <table class="table">
          <thead>
              <tr class="text-nowrap">
              <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :role="role" :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Registration Count <sort-icon :role="role" :sortColumn="sortColumn === 'reg_count'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Course End Date <sort-icon :role="role" :sortColumn="sortColumn === 'end_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                  <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :role="role" :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">Action</th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="(course, key) in displayedItems" :key="key" class="course-row" @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">
              <td class="name">
                  <div class="col-12 d-flex align-items-center">
                  <div class="text-nowrap">{{ course.name }}</div>
                  <div class="ms-2">
                  <course-category-badge :category="course.category"></course-category-badge>
                  </div>
                  </div>
                  <div class="col-12 text-grey two-lines">
                  {{ course.description }}
                  </div>
              </td>
              <td class="reg_count">
                  {{ course.reg_count }}
              </td>
              <td class="end_date">
                  <div class="col-12">
                  {{ course.end_date }}
                  </div>
                  <div class="col-12 text-grey">
                  {{ course.end_time }}
                  </div>
              </td>
              <td class="closing_date">
                  <div class="col-12">
                  {{ course.closing_date }}
                  </div>
                  <div class="col-12 text-grey">
                  {{ course.closing_time }}
                  </div>
              </td>
              <td><course-action action="edit"></course-action></td>
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

      <vue-awesome-paginate
        v-model="localCurrentPage"
        :totalItems="courses.length"
        :items-per-page="1"
        @page-change="handlePageChange"
        class="justify-content-center pagination-container"
      />

  </div>
</template>
  
<script>
import courseAction from '../../components/course/courseAction.vue';
import courseCategoryBadge from '../../components/course/courseCategoryBadge.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';

export default {
  components: {
    courseAction,
    courseCategoryBadge,
    sortIcon,
    modalCourseContent,
    VueAwesomePaginate
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
        status: 'Available',
        action: 'edit',
        available_slots: 10,
        reg_count: 13
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
        status: 'nil',
        action: 'edit',
        available_slots: 10,
        reg_count: 20
        },
      ],
      sortColumn: 'name',
      sortDirection: 'asc',
      role: 'admin',
      selectedCourse: null,
      itemsPerPage: 1,
      localCurrentPage: 1
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
    displayedItems() {
      const startIndex = (this.localCurrentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.courses.slice(startIndex, endIndex);
    }
  }
  }
</script>


<style>
  @import '../../assets/css/course.css';
  @import '../../assets/css/paginate.css';
</style>