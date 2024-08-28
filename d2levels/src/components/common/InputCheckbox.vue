<template>
  <label class="checkbox">
    <input
      type="checkbox"
      v-model="value" />
    <div class="checkbox-icon"></div>
    <div class="checkbox-content">
      <slot></slot>
    </div>
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  modelValue: any,
  readonly?: boolean,
}
const props = defineProps<Props>();

interface Emits {
  (e: 'onChange', evt: any): void,
  (e: 'update:modelValue', evt: any): void,
}
const emit = defineEmits<Emits>();

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    if (!props.readonly) {
      emit('update:modelValue', value);
    }
  }
});

</script>

<style scoped lang="scss">
.checkbox {
  display: flex;
  align-items: center;
  position: relative;
  font-size: 12px;
  line-height: 1;
  cursor: pointer;

  input {
    display: none;
  }

  .checkbox-icon {
    position: relative;
    width: 16px;
    height: 16px;
    background-color: rgb(14, 14, 14);
    border: 1px solid rgb(50, 50, 50);
    border-radius: 5px;
    margin-right: 5px;

    &::after {
      content: '';
      display: block;
      position: absolute;
      top: 50%;
      left: 50%;
      width: 40%;
      height: 80%;
      border: 2px solid var(--color-primary);
      border-top-color: transparent;
      border-left-color: transparent;
      transform: translate(-50%, -70%) rotate(45deg);
      opacity: 0;
    }
  }

  input:checked + .checkbox-icon {
    &::after {
      opacity: 1;
    }
  }

  .checkbox-content {
    display: flex;
    user-select: none;
  }
}

.hex-text {
  $v-padding: 1px;
  $h-padding: 5px;

  display: inline-block;
  position: relative;
  background-color: rgb(14, 14, 14);
  border: 1px solid rgb(50, 50, 50);
  border-radius: 5px;
  line-height: 1.25;
  padding: $v-padding $h-padding;

  .hex, .dec {
    display: inline-block;
  }

  .hex-em {
    font-style: normal;
    opacity: 0.5;
    margin-right: 2px;
  }

  .dec {
    position: absolute;
    right: $h-padding;
    top: $v-padding;
  }
}
</style>
