import type { LevelsTxt } from '@/lib/LevelsTxt';
import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => {
    return {
      'filename': '',
      'act': 0,
      'difficulty': 0,
      'selectedLevel': ({} as LevelsTxt),
    }
  },
  actions: {
  },
  getters: {
  }
});