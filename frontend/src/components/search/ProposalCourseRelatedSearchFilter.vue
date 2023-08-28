<template>
    <div id="searchfitler">
        <div class="container mt-5 mb-5">
            <form>
                <div class="row">
                    <div class="col-sm">
                        <input-field v-model="courseName" type="text" placeholder="Course Name"/>
                    </div>
                    <div class="col-sm">
                        <dropdown-field
                        v-model="category"
                        :default-placeholder="'Course Category'">
                        <option v-for="option in categoryDropdownOptions" :key="option.coursecat_ID" :value="option.coursecat_ID">{{ option.coursecat_Name }}</option>
                        </dropdown-field>
                    </div>
                    <div class="col-sm col-lg-3">
                        <div class="d-flex justify-content-between">
                            <button @click="resetFilter" class="btn" id="resetbtn">Clear All</button>
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
import InputField from "../InputField.vue";
import DropdownField from "../DropdownField.vue";
import CourseService from "@/api/services/CourseService.js"
import CourseCategoryService from "@/api/services/CourseCategoryService.js"

export default({
    name: "SearchFilter",
    data() {
        return {
            courseName: "",
            category: "",
            categoryDropdownOptions: [],
        };
    },
    components: {
        InputField,
        DropdownField,
    },
    async mounted() {
        await this.getAllCourses();
        // await this.searchFilterCourses();
        await this.fetchCategoryDropdownOptions();
    },
    props: {
        searchApi: Function,
    },
    methods: {
        async getAllCourses() {
            let response = await CourseService.getAllCourses();
            this.courseList = response.data.course;
        },
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
        },
        async searchFilter() {
            try {
                const course_Name = this.courseName;
                const coursecat_ID = this.category;

                let searchResults;

                searchResults = await this.searchApi(course_Name, coursecat_ID);

                this.$emit("search-complete", searchResults);
            } catch (error) {
                console.log("Error fetching info:", error);
            }
            

            // reset filter when user clicks search
            this.resetFilter();
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
