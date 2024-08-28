<template>
  <label class="dropper">
    <input
      ref="InputRef"
      :accept="accept"
      type="file"
      :multiple="multiple"
      @change="onInput" />
    <slot></slot>
  </label>
</template>

<script setup lang="ts">
import { ref, withDefaults } from 'vue';
import { useFileReader } from '@/composables/useFileReader';

interface Props {
  accept: string,
  multiple?: boolean,
  clearOnLoad?: boolean,
  type?: string,
}
const props = withDefaults(defineProps<Props>(), {
  multiple: false,
  clearOnLoad: false,
  type: 'auto',
});

interface Emits {
  (e: 'onLoad', value: any): void,
}
const emit = defineEmits<Emits>();

const InputRef = ref();
const reader = useFileReader();

function onInput(e: any) {
  if (e.target.files) {
    reader.read(e.target.files, props.type).then((res) => {
      emit('onLoad', res);

      if (props.clearOnLoad && InputRef.value) {
        setTimeout(() => {
          if (InputRef.value) {
            InputRef.value.value = "";
          }
        }, 100);
      }
    });
  }
}
</script>

<style scoped lang="scss">
.dropper {
  position: relative;
  align-self: center;
  
  input {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
  }
}

.upload-field {
  width: 100%;
}
</style>
