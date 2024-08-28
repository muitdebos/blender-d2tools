<template>
  <div
    ref="viewportRef"
    class="worldspace-viewer">
    <div
      ref="worldRef"
      class="world"
      :style="`--scale: ${scale}; transform: translate(${offsetX}px, ${offsetY}px);`">
      <div class="world-grid">
        <div
          class="grid grid-100"
          :style="`background-size: ${100 * scale}px ${100 * scale}px`">
        </div>

        <div
          class="grid grid-500"
          :style="`background-size: ${500 * scale}px ${500 * scale}px`">
        </div>

        <div
          class="grid"
          :style="`background-size: ${1000 * scale}px ${1000 * scale}px`">
        </div>

        <div
          class="rng-space"
          :style="`width: ${999 * scale}px; height: ${999 * scale}px;`">
          <span :style="`${scale > 0.1 ? '' : 'display: none;'}`">Reserved for DRLG</span>
        </div>

        <div class="out-of-bounds oob-a"></div>
        <div class="out-of-bounds oob-b"></div>
        <div class="out-of-bounds oob-c"></div>

        <div class="grid-texts">
          <div
            v-for="(gy, iy) in grid1000"
            :key="`gy-${gy}`"
            class="grid-text"
            :style="`top: ${gy * scale}px`">
            <div
              v-for="(gx, ix) in grid1000"
              :key="`gx-${gx}`"
              class="grid-text"
              :style="`left: ${gx * scale}px; opacity: ${(ix === 0 || iy === 0 || scale > 0.1) ? .6 : 0};`">
              <span>{{ gx }}, {{ gy }}</span>
            </div>
          </div>
        </div>
      </div>

      <WorldSpaceLevel
        v-for="(l, idx) in reservedLevels"
        :key="`level-${l.Id}`"
        :level="l"
        :index="idx"
        :scale="scale" />

      <WorldSpaceLevel
        v-for="l in nonReservedLevels"
        :key="`level-${l.Id}`"
        :level="l"
        :scale="scale" />
    </div>
    
    <div class="controls">
      <div class="control" @click="setScale(2)">
        <span>+</span>
      </div>
      <div class="control" @click="setScale(1/2)">
        <span>-</span>
      </div>
    </div>

    <div class="details-bar">
      <span>Cursor: {{ mouse.x }}, {{ mouse.y }}</span>
      <span
        v-if="mouseIsInReserved"
        class="mouse-error">Reserved for DRLG</span>
      <span
        v-if="mouseIsOutOfBounds"
        class="mouse-error">Out of bounds</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

import { type LevelsTxt } from '@/lib/LevelsTxt';
import { useDraggable } from '@/composables/useDraggable';

import WorldSpaceLevel from '@/components/WorldSpaceLevel.vue';
import { useMousePosition } from '@/composables/useMousePosition';

interface Props {
  levels: LevelsTxt[],
}
const props = defineProps<Props>();

const viewportRef = ref();
const worldRef = ref();
let rootBox: DOMRect | null = null;

onMounted(() => {
  rootBox = viewportRef.value.getBoundingClientRect();
});

const reservedLevels = computed(() => props.levels.filter(l => {
  const drlgX = (parseInt(l.OffsetX, 10) || 0) < 1000;
  const drlgY = (parseInt(l.OffsetY, 10) || 0) < 1000;
  return drlgX && drlgY;
}));

const nonReservedLevels = computed(() => props.levels.filter(l => {
  const drlgX = (parseInt(l.OffsetX, 10) || 0) < 1000;
  const drlgY = (parseInt(l.OffsetY, 10) || 0) < 1000;
  return !(drlgX && drlgY);
}));

const mouseIsOutOfBounds = ref(false);
const mouseIsInReserved = ref(false);
const mouse = useMousePosition((pos) => {
  if (rootBox) {
    // Coordinates relative to rootBox
    const _x = pos.x.value - rootBox.x;
    const _y = pos.y.value - rootBox.y;
    
    // Invalid coordinates
    let isInViewport = true;
    if ((_x < 0 || _x > rootBox.width) || (_y < 0 || _y > rootBox.height)) {
      isInViewport = false;
    }

    // Screenspace to worldspace
    if (scale.value > 0) {
      pos.x.value = Math.round((_x - offsetX.value) * (1 / scale.value));
      pos.y.value = Math.round((_y - offsetY.value) * (1 / scale.value));
    }

    // Is out of bounds check
    const checkA = pos.x.value - pos.y.value < 4096;
    const checkB = pos.y.value - pos.x.value < 4096;
    const checkC = pos.x.value + pos.y.value < 8191;
    const checkD = pos.y.value - pos.x.value > -4096;
    const checkE = pos.x.value > 0 && pos.y.value > 0;
    mouseIsOutOfBounds.value = isInViewport && !(checkA && checkB && checkC && checkD && checkE);
    mouseIsInReserved.value = (pos.x.value > 0 && pos.y.value > 0) && (pos.x.value < 1000 && pos.y.value < 1000);

    if (!isInViewport) {
      pos.x.value = -1;
      pos.y.value = -1;
    }
  }
});

const grid1000 = [0, 1000, 2000, 3000, 4000, 5000, 6000];

const scale = ref(0.1);
const offsetX = ref(0);
const offsetY = ref(0);
let _startX = 0;
let _startY = 0;

function setScale(multiplier: number) {
  const oldscale = scale.value;
  scale.value = Math.round(scale.value * multiplier * 10000) / 10000;
  const scalediff = scale.value - oldscale;

  if (rootBox) {
    const offX = ((-1 * offsetX.value) + (rootBox.width / 2)) / oldscale;
    offsetX.value += offX * scalediff * -1;

    const offY = ((-1 * offsetY.value) + (rootBox.height / 2)) / oldscale;
    offsetY.value += offY * scalediff * -1;
  }
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

const { isInteracting } = useDraggable(viewportRef, worldRef, {
  onDragStart: (e) => {
    if (viewportRef.value) {
      rootBox = viewportRef.value.getBoundingClientRect();
      _startX = offsetX.value;
      _startY = offsetY.value;
    }
  },
  onDragMove: (e) => {
    if (rootBox) {
      const pctX = clamp(e.drag.diff_percent.x * 100, -100, 100) / 100;
      offsetX.value = _startX + (pctX * rootBox.width);

      const pctY = clamp(e.drag.diff_percent.y * 100, -100, 100) / 100;
      offsetY.value = _startY + (pctY * rootBox.height);
    }
  },
  onDragEnd: (e) => {
    //
  },
});

</script>


<style scoped lang="scss">
$oobFar: 6143px;
$oobNear: 2047px;
$oobDiff: 4096px;
$oobDiff2: 2048px;
$oobDiff4: 1024px;

.worldspace-viewer {
  position: absolute;
  width: 100%;
  background-color: var(--color-worldmap-background);
  overflow: hidden;

  &::before {
    content: '';
    display: block;
    padding-bottom: 100%;
  }
}

.world-grid {
  position: absolute;
  top: 0;
  left: 0;
  width: 200vw;
  height: 200vh;
  pointer-events: none;

  .rng-space {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    top: 1px;
    left: 1px;
    text-align: center;
    color: rgba(255, 0, 0, 0.7);
    background-color: var(--color-worldmap-disabled);
    font-size: 0.5rem;
    font-weight: bold;
    text-transform: uppercase;
  }

  .out-of-bounds {
    position: absolute;
    border: 0px solid var(--color-worldmap-disabled);

    &.oob-a {
      top: calc($oobNear * var(--scale));
      left: calc($oobNear * var(--scale));
      border-width: calc($oobDiff2 * var(--scale));
      border-left-color: transparent;
      border-top-color: transparent;
    }

    &.oob-b {
      top: calc($oobDiff * var(--scale));
      left: 0;
      border-width: calc($oobDiff4 * var(--scale));
      border-right-color: transparent;
      border-top-color: transparent;
    }

    &.oob-c {
      top: 0;
      left: calc($oobDiff * var(--scale));
      border-width: calc($oobDiff4 * var(--scale));
      border-left-color: transparent;
      border-bottom-color: transparent;
    }
  }

  .grid {
    position: absolute;
    top: 0;
    left: 0;
    width: calc($oobFar * var(--scale));
    height: calc($oobFar * var(--scale));
    background-image:
      linear-gradient(to right, var(--color-worldmap-grid) 1px, transparent 1px),
      linear-gradient(to bottom, var(--color-worldmap-grid) 1px, transparent 1px);

    &.grid-500 {
      background-image:
        linear-gradient(to right, var(--color-worldmap-grid) 1px, transparent 1px),
        linear-gradient(to bottom, var(--color-worldmap-grid) 1px, transparent 1px);
    }

    &.grid-100 {
      background-image:
        linear-gradient(to right, var(--color-worldmap-grid) 1px, transparent 1px),
        linear-gradient(to bottom, var(--color-worldmap-grid) 1px, transparent 1px);
    }
  }

  .grid-text {
    position: absolute;
    top: 0px;
    font-size: 0.75rem;
    line-height: 1;
    white-space: nowrap;
    color: var(--color-worldmap-gridtext);

    &.t-ar {
      left: 0px;
    }
  }
}

.world {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  will-change: transform;
}

.controls {
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 0;
  right: 0;
  padding: 0.5rem;

  .control {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 2rem;
    height: 2rem;
    border: 1px solid var(--color-border);
    border-bottom-color: var(--color-border-bottom);
    background-color: var(--color-primary-transparent);
    cursor: pointer;
    user-select: none;

    &:hover {
      background-color: var(--color-primary-transparent-hover);
    }

    + .control {
      margin-top: 0.5rem;
    }
  }
}

.details-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  background-color: var(--color-worldmap-disabled);
  font-size: 12px;
  text-transform: uppercase;
  padding: 0 6px;
  color: rgba(255, 255, 255, 0.7);

  > * + * {
    margin-left: 1rem;
  }

  .mouse-error {
    color: rgba(255, 0, 0, 0.7);
  }
}

</style>
