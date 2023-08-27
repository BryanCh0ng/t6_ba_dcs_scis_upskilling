<template>
    <div id="searchfitler">
        <div class="container mt-5 mb-5">
            <form class="searchform">
                <div class="row d-flex justify-content-center">
                    <div class="col-sm col-lg-5">
                        <input-field v-model="studentName" type="text" placeholder="Student Name"/>
                    </div>
                    <div class="col-sm col-lg-3">
                        <button @click.prevent="searchFilter" class="btn" id="searchbtn">Search</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
// import { axiosClient } from "../api/axiosClient";
import InputField from "../InputField.vue";

export default({
    name: "SearchFilter",
    data() {
        return {
            studentName: "",
        };
    },
    components: {
        InputField,
    },
    methods: {
        searchFilter() {
        //     console.log(this.instructorName);
        //     console.log(this.organizationName);

        }
    }
})
</script>

<style scoped>
    .searchform {
        position: relative;
        left: 7%;
    }
    #searchbtn {
        width: 48%;
        height: 45px;
        border-radius: 10px;
        background-color: #151c55;
        color: #FFFFFF;
    }

</style>
