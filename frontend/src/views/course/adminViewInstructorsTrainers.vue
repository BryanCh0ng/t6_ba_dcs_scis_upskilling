<template>
  <div>
    <search-filter
        :status-options="statusOptions"
        :search-api="getAllInstructorsAndTrainers"
        @search-complete="handleSearchComplete" />

    <div class="container col-12 table-responsive">
      <h5 class="pb-3">All Instructors/Trainers Database</h5>
      <div v-if="instructors_trainers && instructors_trainers.length > 0">
        <table class="table bg-white">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('user_Name')">Name <sort-icon :sortColumn="sortColumn === 'user_Name'" :sortDirection="getSortDirection('user_Name')"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('role_Name')">Role <sort-icon :sortColumn="sortColumn === 'role_Name'" :sortDirection="getSortDirection('role_Name')"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark" @click.prevent="sort('organisation_Name')">Organization <sort-icon :sortColumn="sortColumn === 'organisation_Name'" :sortDirection="getSortDirection('organisation_Name')"/></a></th>
              <th>Ratings</th>
              <th scope="col">Feedback Analysis</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(instructor_trainer, key) in displayedInstructorsTrainers" :key="key">
              <td class="user_name">
                {{ instructor_trainer.user_Name }}
              </td>
              <td class="user_role">
                {{ instructor_trainer.role_Name }}
              </td>
              <td class="orgnanization">
                {{ instructor_trainer.organisation_Name }}
              </td>
              <td class="ratings">
                {{ instructor_trainer.ratings }}
              </td>
              <td><a class="text-nowrap text-dark text-decoration-underline view-feedback-analysis">View Feedback Analysis</a></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="instructors_trainers=[]">
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-if="instructors_trainers.length/itemsPerPage > 0" v-model="localCurrentPageInstructorsTrainers" :totalItems="instructors_trainers.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeInstructors" class="justify-content-center pagination-container"/>
  </div>
</template>
    
<script>
import sortIcon from '@/components/common/sort-icon.vue';
import { VueAwesomePaginate } from 'vue-awesome-paginate';
import SearchFilter from "@/components/search/InstructorRelatedSearchFilter.vue";
import CourseService from "@/api/services/CourseService.js";

export default {
  components: {
    sortIcon,
    VueAwesomePaginate,
    SearchFilter
  },
  data() {
    return {
      instructors_trainers: [],
      sortColumn: '',
      sortDirection: 'asc',
      itemsPerPage: 10,
      localCurrentPageInstructorsTrainers: 1,
      statusOptions: ["Instructor", "Trainer"],
    }
  },
  methods: {
    handlePageChangeInstructors(newPage) {
      this.localCurrentPageInstructors = newPage;
      this.$emit('page-change', newPage);
    },
    async handleSearchComplete(searchResults) {
      // console.log(searchResults)
      this.courses = searchResults;
    },
    async getAllInstructorsAndTrainers(user_Name, role_Name, organizationName) {
      try {
        let response = await CourseService.getAllInstructorsAndTrainers(
          user_Name,
          role_Name,
          organizationName
        );
        this.instructors_trainers = response.data;
        return this.instructors_trainers;
      } catch (error) {
        console.error("Error fetching info:", error);
        throw error;
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
      let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.instructors_trainers)
        if (sort_response.code == 200) {
          this.instructors_trainers = sort_response.data
        }
    }
  },
  computed: {
    displayedInstructorsTrainers() {
      const startIndex = (this.localCurrentPageInstructorsTrainers - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.instructors_trainers.slice(startIndex, endIndex);
    }
  },
  async created() {
    try {
      let response = await CourseService.getAllInstructorsAndTrainers(null, null, null)
      this.instructors_trainers = response.data
    } catch (error) {
      console.error("Error fetching course details:", error);
    }
  }
  }
</script>
  
<style>
  @import '../../assets/css/paginate.css';
</style>