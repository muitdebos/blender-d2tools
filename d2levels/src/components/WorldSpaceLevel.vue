<template>
  <div
    class="level"
    :style="levelStyle"
    @click="selectLevel">
    <div 
      class="level-content"
      :style="`opacity: ${scale > 0.1 ? 1 : 0.1};`">
      {{ level.Name }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

import { type LevelsTxt, getLevelStatsByDifficulty } from '@/lib/LevelsTxt';
import { useSettingsStore } from '@/stores/settings';

const $settings = useSettingsStore();

interface Props {
  level: LevelsTxt
  index?: number
  scale: number
}
const props = defineProps<Props>();

const levelStyle = computed(() => {
  const diffStats = getLevelStatsByDifficulty(props.level, $settings.difficulty);

  let offsetX = `left: ${(parseInt(props.level.OffsetX, 10) || 0) * props.scale}px;`;
  let offsetY = `top: ${(parseInt(props.level.OffsetY, 10) || 0) * props.scale}px;`;
  let sizeX = `width: ${(parseInt(diffStats.sizeX, 10) || 0) * props.scale}px;`;
  let sizeY = `height: ${(parseInt(diffStats.sizeY, 10) || 0) * props.scale}px;`;

  if (typeof props.index !== 'undefined') {
    offsetX = `left: ${-200 * props.scale}px;`;
    offsetY = `top: ${(50 + (300 * props.index)) * props.scale}px;`;
  }

  return `${offsetY} ${offsetX} ${sizeX} ${sizeY}`;
});

function selectLevel() {
  $settings.selectedLevel = props.level;
}

</script>


<style scoped lang="scss">
$borderSize: 50px;

.level {
  position: absolute;
  z-index: 1;
  display: flex;
  font-size: 0.75rem;
  cursor: pointer;

  &:hover {
    z-index: 10;
    background-color: var(--color-primary-hover);

    .level-content {
      opacity: 1 !important;
    }
  }

  &::before {
    content: '';
    display: block;
    position: absolute;
    z-index: -10;
    top: calc(-#{$borderSize} * var(--scale));
    left: calc(-#{$borderSize} * var(--scale));
    width: calc(100% + calc(2*$borderSize * var(--scale)));
    height: calc(100% + calc(2*$borderSize * var(--scale)));
    background-color: rgba(0, 0, 0, 0.1);
    background-image: repeating-linear-gradient(
      -45deg,
      rgba(188, 96, 96, 0.2),
      rgba(188, 96, 96, 0.2) 10px,
      rgba(152, 70, 70, 0.2) 10px,
      rgba(152, 70, 70, 0.2) 20px);
  }

  &::after {
    content: '';
    display: block;
    position: absolute;
    z-index: -9;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--color-primary);
  }

  .level-content {
    pointer-events: none;
    white-space: nowrap;
  }
}
</style>
