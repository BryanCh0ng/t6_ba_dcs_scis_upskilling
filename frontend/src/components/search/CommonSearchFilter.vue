<template>
    <div id="commonsearchfilter">
        <div class="container mt-5 mb-5">
            <form>
                <div class="row">
                    <div class="col-md">
                        <input v-model="courseName" type="text" placeholder="Course Name" class="form-control border-0 shadow-sm px-4 field mb-3"/>

                    </div>
                    <div class="col-md">
                        <dropdown-field
                        v-model="category"
                        :default-placeholder="'Course Category'">
                        <option v-for="option in categoryDropdownOptions" :key="option.coursecat_ID" :value="option.coursecat_ID">{{ option.coursecat_Name }}</option>
                        </dropdown-field>
                    </div>
                    <div class="col-md">
                        <dropdown-field
                        v-model="status"
                        :default-placeholder="'Status'">
                        <option v-for="option in statusDropdownOptions" :key="option" :value="option">{{ option }}</option>
                        </dropdown-field>
                    </div>
                    <div class="col-md">
                        <div class="d-flex justify-content-between">
                            <button @click="resetFilter" class="btn" id="resetbtn" type="button">Clear All</button>
                            <button @click.prevent="searchFilter" class="btn" id="searchbtn">Search</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
// import { axiosClient } from "../api/axiosClient";
import DropdownField from "../DropdownField.vue";
// import InputField from "../InputField.vue";
// import CourseService from "@/api/services/CourseService.js"
import CourseCategoryService from "@/api/services/CourseCategoryService.js"
import UserService from "@/api/services/UserService.js"

export default({
    name: "SearchFilter",
    data() {
        return {
            courseName: "",
            category: "",
            status: "",
            placeholder: "Course Name",
            categoryDropdownOptions: [],
            statusDropdownOptions: [],
        };
    },
    props: {
        statusOptions: Array, 
        searchApi: Function,
    },
    components: {
        DropdownField,
        // InputField,
    },
    async mounted() {
        // await this.getAllCourses();
        // await this.searchFilterCourses();
        await this.fetchCategoryDropdownOptions();
        this.statusDropdownOptions = this.statusOptions;
    },
    methods: {
        // async getAllCourses() {
        //     let response = await CourseService.getAllCourses();
        //     this.courseList = response.data.course;
        // },
        async fetchCategoryDropdownOptions() {
            try {
                const categoryOptions = await CourseCategoryService.getAllCourseCategory(); // Use the CourseCategoryService
                this.categoryDropdownOptions = categoryOptions;
            } catch (error) {
                console.error('Error fetching category dropdown options:', error);
            }
        },
        resetFilter() {
            this.courseName = "";
            this.category = "";
            this.status = "";
            this.placeholder="Course Name"

            this.searchFilter();
        },
        async searchFilter() {
            try {
                const user_ID = await UserService.getUserID()
                const course_Name = this.courseName;
                const coursecat_ID = this.category;
                const status = this.status;

                let searchResults;
                // console.log(status)
                
                // Use the searchApi function from the parent component
                searchResults = await this.searchApi(user_ID, course_Name, coursecat_ID, status);
                
                // Emit the search-complete event to the parent component
                this.$emit("search-complete", searchResults);
            } catch (error) {
                console.log("Error fetching info:", error);
            }

        }
    }
})
</script>

<style scoped>
    .btn {
        width: 48%;
        height: 50px;
        border-radius: 10px;
    }

    #searchbtn {
        background-color: #151c55;
        color: #FFFFFF;
    }

    #resetbtn {
        background-color: transparent;
        border: 3px solid #616161;
        color:black;
    }

</style>
