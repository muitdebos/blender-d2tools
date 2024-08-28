<template>
  <main class="view">    
    <div class="file-uploaders">
      <FileUpload
        accept=".txt,.csv"
        :clearOnLoad="true"
        @onLoad="openLevelsTxt">
        <FullButton
          class="small">
          <span>Import Levels.txt</span>
          <FileText
            :size="12"
            class="icon-right" />
        </FullButton>
      </FileUpload>

      <InputSelect 
        label="Act"
        :value="act"
        :options="actOptions"
        @onUpdate="updateAct"/>

      <InputSelect 
        label="Difficulty"
        :value="difficulty"
        :options="difficultyOptions"
        @onUpdate="updateAct"/>

      <span>Levels: {{ actLevels.length }}</span>
    </div>

    <div class="content">
      <div class="viewer">
        <WorldSpaceViewer
          :levels='actLevels' />
      </div>

      <div class="level-browser">
        <pre
          v-if="$settings.selectedLevel"
          class="level-details">
          {{ $settings.selectedLevel }}
        </pre>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Save, FolderUp, FileText, Plus, SortDesc } from 'lucide-vue-next';

import { type LevelsTxt } from '@/lib/LevelsTxt';

import WorldSpaceViewer from '@/components/WorldSpaceViewer.vue';
import FileUpload from '@/components/common/FileUpload.vue';
import FullButton from '@/components/common/FullButton.vue';
import InputSelect from '@/components/common/InputSelect.vue';
import { useSettingsStore } from '@/stores/settings';

const $settings = useSettingsStore();

const levels = ref(([] as LevelsTxt[]));

function openLevelsTxt(res: LevelsTxt[][]) {
  levels.value = res[0];
}

const act = computed(() => { return $settings.act; });
const actLevels = computed(() => levels.value.filter(l => (parseInt(l['Act'], 10) || 0) === act.value))

const acts = [0, 1, 2, 3, 4]
const actOptions = acts.map(a => ({
  key: `${a}`,
  value: a,
  text: `${a}`,
}));

function updateAct(change: any) {
  $settings.act = change;
}

const difficulty = computed(() => { return $settings.act; });
const difficultyOptions = [{
  key: '0',
  value: 0,
  text: 'Normal',
}, {
  key: '1',
  value: 1,
  text: 'Nightmare',
}, {
  key: '2',
  value: 2,
  text: 'Hell',
}];

function updateDifficulty(change: any) {
  $settings.difficulty = change;
}
</script>


<style scoped lang="scss">
.view {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100vh;
  overflow: auto;
}

.file-uploaders {
  display: flex;
  padding: 1rem 2rem;
  border-bottom: 1px solid var(--color-border);

  > * {
    + * {
      margin-left: 1rem;
    }
  }
}

.content {
  display: flex;
  flex: 1;
}

.viewer {
  position: relative;
  flex: 1 1 70%;
}

.level-browser {
  position: relative;
  flex: 1 1 30%;
  overflow: auto;
  padding: 1rem;
}

.level-parsed {
  display: flex;
  flex-direction: column;
}

.level-details {
  position: absolute;
  width: 100%;
  font-size: 0.75rem;
}
</style>
