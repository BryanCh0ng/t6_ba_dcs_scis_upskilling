<template>
  <div>
    <div class="col-12">
      {{ convertDate(date) }}
    </div>
  </div>
</template>
    
<script>
import {convertDate} from '@/scripts/common/convertDateTime.js'

export default {
props: {
    date: String,
},
methods: {
    convertDate
}
};
</script>