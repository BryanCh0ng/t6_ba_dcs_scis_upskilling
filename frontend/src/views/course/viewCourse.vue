<template>
  <div>
    <search-filter :role="role"></search-filter>

    <div class="pt-5 container col-12 table-responsive">
      <h5 class="pb-3">Courses Available for Registration</h5>

      <div v-if="courses.length > 0">
        <table class="table">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course Name / Description <sort-icon :role="role" :sortColumn="sortColumn === 'name'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course Start Date <sort-icon :role="role" :sortColumn="sortColumn === 'start_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Course End Date <sort-icon :role="role" :sortColumn="sortColumn === 'end_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Closing Date <sort-icon :role="role" :sortColumn="sortColumn === 'closing_date'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(course, key) in courses" :key="key" class="course-row" @click="openModal(course)" data-bs-toggle="modal" data-bs-target="#course_details_modal">
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
              <td class="start_date">
                <div class="col-12">
                  {{ course.start_date }}
                </div>
                <div class="col-12 text-grey">
                  {{ course.start_time }}
                </div>
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
              <td><course-action :action="course.action"></course-action></td>
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

  </div>
</template>

<script>
import searchFilter from "../../components/searchFilter.vue"
import courseAction from '../../components/course/courseAction.vue';
import courseCategoryBadge from '../../components/course/courseCategoryBadge.vue';
import sortIcon from '../../components/common/sort-icon.vue';
import modalCourseContent from '../../components/course/modalCourseContent.vue';

export default {
  components: {
    searchFilter, 
    courseAction,
    courseCategoryBadge,
    sortIcon,
    modalCourseContent,
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
          action: "hopOn",
          fee: 50,
          venue: 'SCIS SR-2',
          format: 'Physical',
          status: 'Available',
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
          action: "shoutOut",
          fee: 100,
          venue: 'SCIS SR-5',
          format: 'Online',
          status: 'nil',
          available_slots: 15
        },
      ],
      sortColumn: 'name',
      sortDirection: 'asc',
      role: 'admin',
      selectedCourse: null
    }
  },
  computed: {
    pageCount() {
      return Math.ceil(this.items.length / this.perPage);
    },
    paginatedItems() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.items.slice(startIndex, endIndex);
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
    }
  }
};
</script>

<style>
  @import '../../assets/css/course.css';
</style>