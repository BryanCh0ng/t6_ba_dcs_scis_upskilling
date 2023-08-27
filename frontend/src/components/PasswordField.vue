<template>
  <div class="input-group password-field">
    <input
      :value="localValue"
      :type="showPassword ? 'text' : 'password'"
      :placeholder="placeholder"
      class="form-control border-0 shadow-sm px-4 field"
      @input="updateLocalValue"
    />
    <div class="input-group-append">
      <div class="input-group-text eye-icon-container">
        <span @click="togglePasswordVisibility" class="eye-icon">
          <font-awesome-icon
            :icon="showPassword ? ['fas', 'eye'] : ['fas', 'eye-slash']"
          />
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  props: {
    value: String,
    placeholder: String
  },
  setup(props, { emit }) {
    const showPassword = ref(false);
    const localValue = ref(props.value);

    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
    };

    const updateLocalValue = event => {
      localValue.value = event.target.value;
      emit('update:value', localValue.value);
    };

    // Watch for changes in the parent's value prop and update the localValue
    watch(() => props.value, newValue => {
      localValue.value = newValue;
    });

    return {
      showPassword,
      localValue,
      togglePasswordVisibility,
      updateLocalValue
    };
  }
};
</script>

<style>
/* For the visibility of the password */
.password-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: black;
}

.eye-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%; /* Match the height of the input field */
  padding-right: 8px; /* Add spacing between the input and the icon */
  cursor: pointer;
  border-top-left-radius: 0px;
  border-bottom-left-radius: 0px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  background-color: white;
  border: 0px;
  width: 40px;
}
</style>
