<template>
  <div
    class="hex-text"
    :class="ishex ? 'is-hex' : 'is-dec'">
    <span class="hex">
      <em class="hex-em">0x</em>{{ hex }}
    </span>
    <span class="dec">{{ dec }}</span>
  </div>
</template>

<script setup lang="ts">
import { dec2hex, hex2dec, zp } from '@/lib/utils';
import { computed } from 'vue';

interface Props {
  value: number | string,
  zeropad?: number,
}
const props = defineProps<Props>();

const ishex = computed(() => typeof props.value === "string" );
const hex = computed(() => typeof props.value === "string" ? props.value : zp(dec2hex(props.value), (props.zeropad || 1)));
const dec = computed(() => typeof props.value === "number" ? props.value : hex2dec(props.value));

</script>

<style scoped lang="scss">
@mixin toggle($state) {
  @if $state == 1 {
    opacity: 1;
  }
  @else {
    opacity: 0;
    pointer-events: none;
  }
}
.hex-text {
  $v-padding: 1px;
  $h-padding: 5px;

  display: inline-block;
  position: relative;
  // background-color: rgba(255, 255, 255, 0.05);
  background-color: rgb(14, 14, 14);
  border: 1px solid rgb(50, 50, 50);
  border-radius: 5px;
  line-height: 1.25;
  padding: $v-padding $h-padding;

  &.is-hex {
    .dec { @include toggle(0); }
    &:hover {
      .dec { @include toggle(1); }
      .hex { @include toggle(0); }
    }
  }

  &.is-dec {
    .hex { @include toggle(0); }
    &:hover {
      .hex { @include toggle(1); }
      .dec { @include toggle(0); }
    }
  }

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
