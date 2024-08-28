<template>
  <label
    class="wrapper"
    :class="{ 'is-readonly': readonly }">
    <span
      class="label"
      :style="`${labelWidth ? 'flex: 0 0 '+labelWidth+'px;' : ''}`">{{ label }}</span>
    <input
      v-model="value"
      class="input"
      type="text"
      :readonly="readonly" />
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  modelValue: any,
  label?: string,
  labelWidth?: number,
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
$v-padding: 1px;
$h-padding: 5px;

.wrapper {
  display: flex;
  align-items: center;
  height: 21px;
}

.label {
  font-size: 9px;
  font-family: var(--font-family);
  text-transform: uppercase;
  margin-right: 4px;
  white-space: nowrap;
  text-align: right;
  cursor: pointer;
}

.input {
  display: inline-block;
  position: relative;
  // background-color: rgba(255, 255, 255, 0.05);
  background-color: rgb(14, 14, 14);
  border: 1px solid rgb(50, 50, 50);
  border-radius: 5px;
  line-height: 1.25;
  padding: $v-padding $h-padding;
  color: white;
  outline: none;
  width: 100%;

  &:focus {
    border-color: rgb(159, 113, 40);
  }
}
</style>
