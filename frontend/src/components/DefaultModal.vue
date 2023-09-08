<template>
    <div v-if="OpenClose" class="modal fade show custom-modal-backdrop" tabindex="1" aria-labelledby="exampleModalLabel" aria-modal="true" role="dialog" style="display:block;">
         <div class="modal-dialog">
             <div class="modal-content">
                 <div class="modal-header">
                     <h5 class="modal-title">{{ title }}</h5>
                     <button type="button" class="btn-close" @click="OpenCloseFun()" aria-label="Close"></button>
                 </div>
                 <div class="modal-body">
                     <p>{{ message }}</p>
                 </div>
                 <div class="modal-footer">
                     <button type="button" @click="OpenCloseFun()" :class="'btn btn-' + variant">Close</button>
                 </div>
             </div>
         </div>
     </div>
 </template>
 <script>
 export default {
     name: 'DefaultModal',
     props: {
         //Prop to control modal visibility 
         visible: Boolean,
         message: String,
         title: String,
         //Prop for customizing the button style 
         variant: String,
         
     },
     data() {
         return {
             //It sets 'OpenClose' based on the initial value (false) of the 'visible' prop to determine if the modal should be initially open or closed 
             OpenClose: this.visible,
         }
     },
     methods: {
         //This method is triggered when the close button in the modal is clicked, allowing the modal to be closed 
         OpenCloseFun() {
             this.OpenClose = false;
 
             //Reset the body scrollbar
             document.body.style.overflowY = 'auto';
 
             //Pass value to the parent vue component
             this.$emit('modal-closed', this.OpenClose);
         }
     },
     //Listens for changes in the 'visible' prop
     watch: {
         visible: function (newVal) {
             //When the prop changes, it updates the 'OpenClose' property to reflect the new value (This ensures that the modal's state is synchronized with the changes in the 'visible' prop)
             this.OpenClose = newVal
 
             if(this.OpenClose) {
                 //Hide the body scrollbar
                 document.body.style.overflowY = 'hidden';
             }
         }
     }
 }
 </script>
 
 <style scoped>
 .custom-modal-backdrop {
   background-color: rgba(0, 0, 0, 0.5); /* Adjust the opacity as needed */
   position: fixed;
   top: 0;
   left: 0;
   width: 100%;
   height: 100%;
   z-index: 1050; /* Set the z-index to be higher than the modal's z-index */
 }
 
 </style>