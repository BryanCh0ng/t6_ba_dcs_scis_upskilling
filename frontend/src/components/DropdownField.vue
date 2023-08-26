<template>
    <select v-model="selectedValue" class="form-select border-0 shadow-sm px-4 field">
        <option disabled hidden value="">{{ defaultPlaceholder }}</option>
        <slot></slot>
    </select>
</template>
  
<script>
import { ref, watch } from 'vue';

export default {
    props: {
        modelValue: String,
        defaultPlaceholder: String,
    },
    setup(props, { emit }) {
        const selectedValue = ref(props.modelValue || '');

        watch(
            () => props.modelValue,
            (newValue) => {
                selectedValue.value = newValue;
            }
        );

        watch(selectedValue, (newValue) => {
            emit('update:modelValue', newValue);
        });

        return {
            selectedValue,
        };
    },
};
</script>
  