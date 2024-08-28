import { importLevelsTxt } from '@/lib/LevelsTxt';

export function useFileReader() {
  function read(files: FileList, type = 'auto') {
    if (files.length > 0) {
      const promises = ([] as any[]);

      for (let i = 0; i < files.length; i++) {
        const file = files.item(i);
        if (file) {
          // const filesplit = file.name.split('.');
          // const fileext = filesplit[filesplit.length - 1];

          promises.push(importLevelsTxt(file));
        }
      }

      return Promise.all(promises);
    }
    return Promise.reject();
  }


  return {
    read,
  }
}
