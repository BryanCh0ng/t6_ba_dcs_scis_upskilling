<template>
  <div>
    <div class="col-12">
      {{ convertDate(date) }}
    </div>
    <div class="col-12 text-grey">
      {{ convertTime(time) }}
    </div>
  </div>
</template>
    
<script>
import {convertDate, convertTime} from '@/scripts/common/convertDateTime.js'

export default {
props: {
    date: String,
    time: String,
},
methods: {
    convertDate, 
    convertTime
}
};
</script>