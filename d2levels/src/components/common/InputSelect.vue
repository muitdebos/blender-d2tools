<template>
  <label
    class="wrapper"
    :class="{ 'is-readonly': readonly }">
    <span
      class="label"
      :style="`${labelWidth ? 'flex: 0 0 '+labelWidth+'px;' : ''}`">{{ label }}</span>

    <select
      v-model="editValue"
      class="select"
      @change="update"
      :readonly="readonly">
      <option
        v-for="option in options"
        :key="`${option.key}`"
        :value="option.value">
        {{ option.text || option.value }}
      </option>
    </select>
  </label>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  value: any,
  options: { key: string, value: any, text?: string }[],
  label?: string,
  labelWidth?: number,
  readonly?: boolean,
}
const props = defineProps<Props>();

interface Emits {
  (e: 'onUpdate', value: any): void,
}
const emit = defineEmits<Emits>();

const editValue = ref(props.value);

function update(e: any) {
  emit('onUpdate', editValue.value);
}

</script>

<style scoped lang="scss">
$v-padding: 1px;
$h-padding: 5px;

.wrapper {
  display: flex;
  align-items: center;
  height: 24px;

  &.is-readonly {
    pointer-events: none;

    .select {
      border: 1px solid var(--color-border);
      border-bottom-color: var(--color-border-bottom);
      background-color: var(--color-primary-transparent);
    }
  }
}

.label {
  font-size: 9px;
  font-family: var(--font-family);
  text-transform: uppercase;
  margin-right: 4px;
  white-space: nowrap;
  text-align: right;
}

.select {
  display: inline-block;
  position: relative;
  border: 1px solid var(--color-border);
  border-bottom-color: var(--color-border-bottom);
  background-color: var(--color-primary-transparent);
  padding: $v-padding $h-padding;
  color: white;
  outline: none;
  width: 100%;
  height: 100%;

  &:focus {
    border-color: var(--color-border-bright)
  }
}
</style>
