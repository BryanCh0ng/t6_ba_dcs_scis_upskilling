<template>
    <div id="searchfitler">
        <div class="container mt-5 mb-5">
            <form class="searchform">
                <div class="row d-flex justify-content-center">
                    <div class="col-md-5">
                        <input v-model="name" type="text" placeholder="Name" class="form-control border-0 shadow-sm px-4 field mb-3"/>
                    </div>
                    
                    <div class="col-md-4">
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
import _ from "lodash";

export default({
    name: "SearchFilter",
    data() {
        return {
            name: "",
        };
    },
    props: {
        searchApi: Function,
    },
    watch: {
        name: _.debounce(function() {
            this.searchFilter();
        }, 300)
    },
    methods: {
        resetFilter() {
            this.name = "";

            this.searchFilter();
        },
        async searchFilter() {
            try {
                const name = this.name;

                let searchResults;

                searchResults = await this.searchApi(name);

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
