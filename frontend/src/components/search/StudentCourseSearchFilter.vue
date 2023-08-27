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
                    <div class="col-sm">
                        <dropdown-field
                        v-model="coursetype"
                        :default-placeholder="'Course Type'">
                        <option value="allcourse">All Course</option>
                        <option value="interest">Hop on</option>
                        <option value="register">Shout out</option>
                        </dropdown-field>
                    </div>
                    <div class="col-sm">
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
import DropdownField from "../DropdownField.vue";
import InputField from "../InputField.vue";
import CourseCategoryService from "@/api/services/CourseCategoryService.js"

export default({
    name: "SearchFilter",
    data() {
        return {
            courseName: "",
            category: "",
            coursetype: "",
            categoryDropdownOptions: [],
        };
    },
    components: {
        DropdownField,
        InputField,
    },
    async mounted() {
        await this.fetchCategoryDropdownOptions(); // Fetch category options using the new service
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
            this.coursetype = "";
        },
        searchFilter() {
            const filters = {
                courseName: this.courseName,
                category: this.category,
                coursetype: this.coursetype,
            };
            this.$emit('apply-filters', filters);
        }
    },
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
        border: 4px solid #616161;
        color:black;
    }

</style>
