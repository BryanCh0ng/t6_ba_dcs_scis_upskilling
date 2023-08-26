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
        searchFilter() {
        //     console.log(this.courseName);
        //     console.log(this.category);

            // reset filter when user clicks search
            this.resetFilter();
        }
    }
})
</script>

<style scoped>
    button {
        width: 48%;
        height: 45px;
        border-radius: 10px;
    }

    #searchbtn {
        background-color: #151c55;
        color: #FFFFFF;
    }

    #resetbtn {
        background-color: transparent;
        border: 4px solid #616161;
    }

</style>
