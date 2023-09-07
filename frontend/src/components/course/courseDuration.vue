<template>
  <div>
    <div class="col-12">
      {{ convertTime(start_time) }} - {{ convertTime(end_time) }}
    </div>
  </div>
</template>
    
<script>
import {convertTime} from '@/scripts/common/convertDateTime.js'

export default {
props: {
    start_time: String,
    end_time: String,
},
methods: {
    convertTime
}
};
</script>