<template>
    <div>
    
      <div class="container col-12 table-responsive">
        <h5 class="pb-3">All Feedback Templates</h5>
        <div v-if="feedback_templates && feedback_templates.length > 0">
          <table class="table bg-white" style="table-layout: fixed;">
            <thead>
              <tr class="text-nowrap">
                <th scope="col">
                  <a href="" @click.prevent="sort('template_Name')" class="text-decoration-none text-dark">Name<sort-icon :sortColumn="sortColumn === 'template_Name'" :sortDirection="getSortDirection('template_Name')"/></a></th>
                <th scope="col">
                  <a href="" @click.prevent="sort('created_On')" class="text-decoration-none text-dark">Created On<sort-icon :sortColumn="sortColumn === 'created_On'" :sortDirection="getSortDirection('created_On')"/></a></th>
                <th scope="col">Action(s)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(feedback_template, key) in displayedFeedbackTemplates" :key="key">
                <td>
                    {{ feedback_template.template_Name }}
                </td>
                <td>
                  {{ convertDate(feedback_template.created_On) }}
                </td>
                <td class="d-flex">
                  <div><button class="btn btn-info apply_to_course text-light font-weight-bold text-nowrap">Apply to Course(s)</button></div>
                  <div><button class="m-4 mt-0 mb-0 btn btn-edit edit text-light font-weight-bold text-nowrap" @click="goToEditFeedbackTemplate(feedback_template.template_ID)">Edit</button></div>
                  <div><button class="btn btn-danger delete text-light font-weight-bold text-nowrap">Delete</button></div>
                </td>
              </tr>               
            </tbody>
          </table>
  
        </div>
        <div v-else-if="feedback_templates=[]">
          <p>No records found</p>
        </div>
      </div>
      <vue-awesome-paginate v-if="feedback_templates.length/itemsPerPage > 0" v-model="localCurrentPageFeedbackTemplates" :totalItems="feedback_templates.length" :items-per-page="itemsPerPage" @page-change="handlePageChangeFeedbackTemplates" class="justify-content-center pagination-container"/>
      
      <!-- <div class="modal fade" id="after_action_modal" tabindex="-1" aria-hidden="true" ref="afterActionModal">
        <div class="modal-dialog modal-lg"> 
          <modal-after-action  @model-after-action-close="modalAfterActionClose" :message="receivedMessage" @close-modal="closeModal" />
        </div>
      </div> -->
  
    </div>
  
  </template>
    
  <script>
  import sortIcon from '@/components/common/sort-icon.vue';
  import { VueAwesomePaginate } from 'vue-awesome-paginate';
  import CourseService from "@/api/services/CourseService.js";
  import FeedbackTemplateService from "@/api/services/FeedbackTemplateService.js";
  import {convertDate} from '@/scripts/common/convertDateTime.js'
  // import modalAfterAction from '@/components/course/modalAfterAction.vue';
  
  export default {
    components: {
      sortIcon,
      VueAwesomePaginate,
      // modalAfterAction
    },
    data() {
      return {
        feedback_templates: [],
        sortColumn: '',
        sortDirection: 'asc',
        selectedCourse: null,
        itemsPerPage: 10,
        localCurrentPageFeedbackTemplates: 1,
        receivedMessage: '',
        actionCourse: {}
      }
    },
    computed: {
      displayedFeedbackTemplates() {
        const startIndex = (this.localCurrentPageFeedbackTemplates - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.feedback_templates.slice(startIndex, endIndex);
      },
    },
    methods: {
      convertDate,
      handlePageChangeFeedbackTemplates(newPage) {
        this.localCurrentPageFeedbackTemplates = newPage;
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
          let response = await FeedbackTemplateService.getAllTemplates()
          this.feedback_templates = response
        } catch (error) {
          console.error("Error fetching feedback template details:", error);
        }
      },
      // modalAfterActionClose() {
      //   this.loadData();
      // },
      sort(column) {
        if (this.sortColumn === column) {
          this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortColumn = column;
          this.sortDirection = 'asc';
        }
        this.sortFeedbackTemplate()
      },
      getSortDirection(column) {
        if (this.sortColumn === column) {
          return this.sortDirection;
        }
      },
      async sortFeedbackTemplate() {
        let sort_response = await CourseService.sortRecords(this.sortColumn, this.sortDirection, this.feedback_templates)
        console.log(sort_response)
          if (sort_response.code == 200) {
            this.feedback_templates = sort_response.data
          }
      },
      goToEditFeedbackTemplate(feedback_template_id) {
        this.$router.push({ name: 'editFeedbackTemplate', params: {id: feedback_template_id}})
      },
    },
    created() {
     this.loadData();
    },
    // mounted() {
    //   const buttonElement = document.createElement('button');
    //   buttonElement.className = 'btn btn-primary d-none invisible-btn';
    //   buttonElement.setAttribute('data-bs-toggle', 'modal');
    //   buttonElement.setAttribute('data-bs-target', '#after_action_modal');
    //   this.$el.appendChild(buttonElement);
    //   const modalElement = this.$refs.afterActionModal;
    //   modalElement.addEventListener('hidden.bs.modal', this.modalAfterActionClose);
    // },
    // beforeUnmount() {
    //   const modalElement = this.$refs.afterActionModal;
    //   modalElement.removeEventListener('hidden.bs.modal', this.modalAfterActionClose)
    // },
    }
  </script>
  
  <style>
    @import '../../assets/css/course.css';
    @import '../../assets/css/paginate.css';
  </style>