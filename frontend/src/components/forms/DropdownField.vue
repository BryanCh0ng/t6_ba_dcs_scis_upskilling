<template>
    <div>
        <select v-model="selectedValue" :class="{ 'form-select': true, 'border-0': !hasError, 'shadow-sm': true, 'px-4': true, 'field': true, 'is-invalid': hasError}" class="custom-select" :disabled="disabled">
            <option disabled hidden value="">{{ defaultPlaceholder }}</option>
            <slot></slot>
        </select>
        <div v-if="hasError" class="text-danger">
            <span v-for="error in errors" :key="error">{{ error }}</span>
        </div>
    </div>
</template>
  
<script>
import { ref, watch } from 'vue';

export default {
    props: {
        modelValue: String,
        defaultPlaceholder: String,
        errors: Array, // Pass errors from parent
        disabled: Boolean
    },
    setup(props, { emit }) {
        const selectedValue = ref(props.modelValue || '');
        const hasError = ref(false);
        const errorMessage = ref('');

        watch(
            () => props.modelValue,
            (newValue) => {
                selectedValue.value = newValue;
            }
        );
         
        // Watch for changes in errors and update hasError and errorMessage accordingly
        watch(() => props.errors, (newErrors) => {
        hasError.value = newErrors && newErrors.length > 0;
        errorMessage.value = hasError.value ? newErrors[0] : '';
        });

        watch(selectedValue, (newSelectedValue) => {
            emit('update:modelValue', newSelectedValue);
        });

        return {
            selectedValue,
            hasError,
            errorMessage,
        };
    },
};
</script>

<style scoped>
.custom-select {
    cursor: pointer !important;
}; 

</style>