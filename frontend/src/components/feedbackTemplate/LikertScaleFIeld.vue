<template>
  <div>
    <label for="">{{ qnNum }}. {{ label }}</label>
    <ul class='likert'>
      <li v-for="option in options" :key="option.id">
        <input type="radio" :name="label" :value="option.option"  v-model="selectedOption">
        <label>{{ option.option }}</label>
      </li>
    </ul>
  </div>
</template>
  
<script>
export default {
  props: {
    label: String,
    id: Number,
    options: Array,
    qnNum: Number
  },
  data() {
    return {
      selectedOption: null
    }
  },
  watch: {
    selectedOption(newValue) {
      this.$emit('input', {value: newValue, key: this.qnNum-1});
    }
  }
};
</script>

<style scoped> .likert {
  list-style:none;
  width:100%;
  margin:0;
  padding:0 0 35px;
  display:block;
  border-bottom:2px solid #efefef;
}
.likert:last-of-type {
  border-bottom:0;
}
.likert:before {
  content: '';
  position:relative;
  top:11px;
  left:9.5%;
  display:block;
  background-color:#efefef;
  height:4px;
  width:78%;
}
.likert li {
  display:inline-block;
  width:19%;
  text-align:center;
  vertical-align: top;
}
.likert li input[type=radio] {
  display:block;
  position:relative;
  top:0;
  left:50%;
  margin-left:-6px;
  
}
.likert li label {
  width:100%;
}

</style>
