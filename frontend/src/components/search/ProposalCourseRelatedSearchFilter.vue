<template>
    <div id="searchfitler">
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
                    <div class="col-md col-lg-3">
                        <div class="d-flex justify-content-between">
                            <button @click="resetFilter" class="btn" id="resetbtn" button="type">Reset</button>
                            <button @click.prevent="searchFilter" class="btn" id="searchbtn">Search</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import DropdownField from "../DropdownField.vue";
import CourseCategoryService from "@/api/services/CourseCategoryService.js";
import _ from "lodash";

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
        DropdownField,
    },
    async mounted() {
        await this.fetchCategoryDropdownOptions();
    },
    props: {
        searchApi: Function,
    },
    watch: {
        courseName: _.debounce(function() {
            this.searchFilter();
        }, 300),
        category() {
            this.searchFilter();
        }
    },
    methods: {
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

            this.searchFilter();
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
