<template>
    <div id="searchfitler">
        <div class="container mt-5 mb-5">
            <form class="searchform">
                <div class="row d-flex justify-content-center">
                    <div class="col-md">
                        <input-field v-model="name" type="text" placeholder="Name"/>
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
                            <button @click="resetFilter" class="btn" id="resetbtn" button="type">Clear</button>
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

export default({
    name: "SearchFilter",
    data() {
        return {
            name: "",
            statusDropdownOptions: this.statusOptions,
            status: this.defaultStatus,
        };
    },
    props: {
        statusOptions: Array, 
        searchApi: Function,
        defaultStatus: String,
    },
    components: {
        InputField,
        DropdownField
    },
    methods: {
        resetFilter() {
            this.name = "";
            this.status = "";

            this.searchFilter();
        },
        async searchFilter() {
            try {
                const name = this.name;
                const status = this.status;

                let searchResults;

                searchResults = await this.searchApi(name, status);

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
