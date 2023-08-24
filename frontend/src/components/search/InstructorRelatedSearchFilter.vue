<template>
    <div id="searchfitler">
        <div class="container mt-5 mb-5">
            <form>
                <div class="row">
                    <div class="col-sm">
                        <input-field v-model="instructorName" type="text" placeholder="Instructor Name"/>
                    </div>
                    <div class="col-sm">
                        <input-field v-model="organizationName" type="text" placeholder="Organization Name"/>
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
import InputField from "../InputField.vue";

export default({
    name: "SearchFilter",
    data() {
        return {
            instructorName: "",
            organizationName: "",
        };
    },
    components: {
        InputField,
    },
    methods: {
        resetFilter() {
            this.instructorName = "";
            this.organizationName = "";
        },
        searchFilter() {
        //     console.log(this.instructorName);
        //     console.log(this.organizationName);

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
