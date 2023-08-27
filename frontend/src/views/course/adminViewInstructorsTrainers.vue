<template>
  <div>
    <div class="pt-5 container col-12 table-responsive" v-if="!loading">
      <h5 class="pb-3">All Instructors/Trainers Database</h5>
      <div v-if="instructors_trainers.length > 0">
        <table class="table">
          <thead>
            <tr class="text-nowrap">
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Name <sort-icon :sortColumn="sortColumn === 'user_name'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Role <sort-icon :sortColumn="sortColumn === 'user_role'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Organization <sort-icon :sortColumn="sortColumn === 'organization'" :sortDirection="sortDirection"/></a></th>
              <th scope="col">
                <a href="" class="text-decoration-none text-dark">Ratings <sort-icon :sortColumn="sortColumn === 'ratings'" :sortDirection="sortDirection"/></a></th>
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
      <div v-else>
        <p>No records found</p>
      </div>
    </div>
    <vue-awesome-paginate v-if="instructors_trainers.length/itemsPerPage > 0" v-model="localCurrentPageInstructorsTrainers" :totalItems="instructors_trainers.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeInstructors" class="justify-content-center pagination-container"/>
  </div>
</template>
    
  <script>
  import sortIcon from '../../components/common/sort-icon.vue';
  import { VueAwesomePaginate } from 'vue-awesome-paginate';
  import { getAllInstructors, getAllTrainers } from '../../scripts/user.js';
  
  export default {
    components: {
      sortIcon,
      VueAwesomePaginate,
    },
    data() {
      return {
        instructors_trainers: [
          {
          "role_Name": "Instructors",
          "user_Email": "christina.lee@smu.edu.sg",
          "user_ID": 4,
          "user_Name": "Christina Lee",
          "user_Password": "christina"
        },
        {
          "role_Name": "Instructor",
          "user_Email": "jennifer.smith@smu.edu.sg",
          "user_ID": 41,
          "user_Name": "Jennifer Smith",
          "user_Password": "jennifer"
        },
        {
          "role_Name": "Instructor",
          "user_Email": "robert.johnson@smu.edu.sg",
          "user_ID": 42,
          "user_Name": "Robert Johnson",
          "user_Password": "robert"
        },
        {
          "role_Name": "Instructor",
          "user_Email": "michelle.williams@smu.edu.sg",
          "user_ID": 43,
          "user_Name": "Michelle Williams",
          "user_Password": "michelle"
        },
        {
          "role_Name": "Instructor",
          "user_Email": "daniel.brown@smu.edu.sg",
          "user_ID": 44,
          "user_Name": "Daniel Brown",
          "user_Password": "danielb"
        },
        {
          "role_Name": "Instructor",
          "user_Email": "laura.davis@smu.edu.sg",
          "user_ID": 45,
          "user_Name": "Laura Davis",
          "user_Password": "laura"
        }
        ],
        sortColumn: 'name',
        sortDirection: 'asc',
        itemsPerPage: 10,
        localCurrentPageInstructorsTrainers: 1,
        loading: true
      }
    },
    methods: {
      handlePageChangeInstructors(newPage) {
        this.localCurrentPageInstructors = newPage;
        this.$emit('page-change', newPage);
      },
    },
    computed: {
      displayedInstructorsTrainers() {
        const startIndex = (this.localCurrentPageInstructorsTrainers - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.instructors_trainers.slice(startIndex, endIndex);
      }
    },
    }
  </script>
  
  
<style>
  @import '../../assets/css/paginate.css';
</style>