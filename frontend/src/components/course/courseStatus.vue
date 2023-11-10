<template>
    <div>
      <span :class="getStatusBadgeClass(status)">{{ status }}</span>
    </div>
  </template>
    
  <script>
  
  export default {
    props: {
      status: String,
    },
    methods: {
    },
    computed: {
      getStatusBadgeClass() {
        return (status) => {
            switch (status) {
            case 'Enrolled':
                return 'mt-1 pt-2 pb-2 badge text-light bg-medium-sea-green';
            case 'Dropped':
                return 'mt-1 pt-2 pb-2 badge text-light bg-crimson';
            case 'Pending':
                return 'mt-1 pt-2 pb-2 badge text-light bg-dark-grey';
            case 'Approved':
                return 'mt-1 pt-2 pb-2 badge text-light bg-medium-sea-green';
            case 'Rejected':
                return 'mt-1 pt-2 pb-2 badge text-light bg-crimson';
            case 'Offered':
                return 'mt-1 pt-2 pb-2 badge text-light bg-medium-sea-green';
            case 'Ongoing':
                return 'mt-1 pt-2 pb-2 badge text-light bg-medium-sea-green';
            case 'Active':
            return 'mt-1 pt-2 pb-2 badge text-light bg-medium-sea-green';
            case 'Retired':
                return 'mt-1 pt-2 pb-2 badge text-light bg-secondary';
            case 'Open for voting':
                return 'mt-1 pt-2 pb-2 badge text-light bg-blue';
            case 'Offered for students to register':
                return 'mt-1 pt-2 pb-2 badge text-light bg-medium-sea-green';
            case 'Inactive':
                return 'mt-1 pt-2 pb-2 badge text-light bg-crimson';
            case 'Present':
                return 'mt-1 pt-2 pb-2 badge text-light bg-medium-sea-green';
            case 'Absent':
                return 'mt-1 pt-2 pb-2 badge text-light bg-crimson';
            case 'Upcoming':
                return 'mt-1 pt-2 pb-2 badge text-light bg-blue';
            case 'Late':
                return 'mt-1 pt-2 pb-2 badge text-light bg-warning';
            default:
                return 'mt-1 pt-2 pb-2 badge text-light bg-secondary';
            } 
        };
      },
    }
}
</script>
