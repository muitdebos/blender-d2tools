import { removeFileExtension, zp } from '@/lib/utils';
import { useFileDownload } from '@/composables/useFileDownload';
import { useSettingsStore } from '@/stores/settings';

export type LevelsTxt = {
  'Name': string
  'Id': string
  'Pal': string
  'Act': string
  'QuestFlag': string
  'QuestFlagEx': string
  'Layer': string
  'SizeX': string
  'SizeY': string
  'SizeX(N)': string
  'SizeY(N)': string
  'SizeX(H)': string
  'SizeY(H)': string
  'OffsetX': string
  'OffsetY': string
  'Depend': string
  'Teleport': string
  'Rain': string
  'Mud': string
  'NoPer': string
  'LOSDraw': string
  'FloorFilter': string
  'BlankScreen': string
  'DrawEdges': string
  'IsInside': string
  'DrlgType': string
  'LevelType': string
  'SubType': string
  'SubTheme': string
  'SubWaypoint': string
  'SubShrine': string
  'Vis0': string
  'Vis1': string
  'Vis2': string
  'Vis3': string
  'Vis4': string
  'Vis5': string
  'Vis6': string
  'Vis7': string
  'Warp0': string
  'Warp1': string
  'Warp2': string
  'Warp3': string
  'Warp4': string
  'Warp5': string
  'Warp6': string
  'Warp7': string
  'Intensity': string
  'Red': string
  'Green': string
  'Blue': string
  'Portal': string
  'Position': string
  'SaveMonsters': string
  'Quest': string
  'WarpDist': string
  'MonLvl1': string
  'MonLvl2': string
  'MonLvl3': string
  'MonLvl1Ex': string
  'MonLvl2Ex': string
  'MonLvl3Ex': string
  'MonDen': string
  'MonDen(N)': string
  'MonDen(H)': string
  'MonUMin': string
  'MonUMax': string
  'MonUMin(N)': string
  'MonUMax(N)': string
  'MonUMin(H)': string
  'MonUMax(H)': string
  'MonWndr': string
  'MonSpcWalk': string
  'NumMon': string
  'mon1': string
  'mon2': string
  'mon3': string
  'mon4': string
  'mon5': string
  'mon6': string
  'mon7': string
  'mon8': string
  'mon9': string
  'mon10': string
  'mon11': string
  'mon12': string
  'mon13': string
  'mon14': string
  'mon15': string
  'mon16': string
  'mon17': string
  'mon18': string
  'mon19': string
  'mon20': string
  'mon21': string
  'mon22': string
  'mon23': string
  'mon24': string
  'mon25': string
  'rangedspawn': string
  'nmon1': string
  'nmon2': string
  'nmon3': string
  'nmon4': string
  'nmon5': string
  'nmon6': string
  'nmon7': string
  'nmon8': string
  'nmon9': string
  'nmon10': string
  'nmon11': string
  'nmon12': string
  'nmon13': string
  'nmon14': string
  'nmon15': string
  'nmon16': string
  'nmon17': string
  'nmon18': string
  'nmon19': string
  'nmon20': string
  'nmon21': string
  'nmon22': string
  'nmon23': string
  'nmon24': string
  'nmon25': string
  'umon1': string
  'umon2': string
  'umon3': string
  'umon4': string
  'umon5': string
  'umon6': string
  'umon7': string
  'umon8': string
  'umon9': string
  'umon10': string
  'umon11': string
  'umon12': string
  'umon13': string
  'umon14': string
  'umon15': string
  'umon16': string
  'umon17': string
  'umon18': string
  'umon19': string
  'umon20': string
  'umon21': string
  'umon22': string
  'umon23': string
  'umon24': string
  'umon25': string
  'cmon1': string
  'cmon2': string
  'cmon3': string
  'cmon4': string
  'cpct1': string
  'cpct2': string
  'cpct3': string
  'cpct4': string
  'camt1': string
  'camt2': string
  'camt3': string
  'camt4': string
  'Themes': string
  'SoundEnv': string
  'Waypoint': string
  'LevelName': string
  'LevelWarp': string
  'EntryFile': string
  'ObjGrp0': string
  'ObjGrp1': string
  'ObjGrp2': string
  'ObjGrp3': string
  'ObjGrp4': string
  'ObjGrp5': string
  'ObjGrp6': string
  'ObjGrp7': string
  'ObjPrb0': string
  'ObjPrb1': string
  'ObjPrb2': string
  'ObjPrb3': string
  'ObjPrb4': string
  'ObjPrb5': string
  'ObjPrb6': string
  'ObjPrb7': string
  'Beta': string
}

export function parseLevelsTxt(b: any): LevelsTxt {
  // console.log(b);
  // const _b = ({} as LevelsTxt);
  // _b.block = parseInt(b.block, 10);
  // _b.pcx_file = b.pcx_file;
  // _b.pcx_x = parseInt(b.pcx_x, 10);
  // _b.pcx_y = parseInt(b.pcx_y, 10);
  // _b.direction = asDWord(b.direction);
  // _b.roof_y = parseInt(b.roof_y, 10);
  // _b.tile_sound = parseInt(b.tile_sound, 10);
  // _b.animated = parseInt(b.animated, 10);
  // _b.orientation = asDWord(b.orientation);
  // _b.main_index = asDWord(b.main_index);
  // _b.sub_index = asDWord(b.sub_index);
  // _b.frame = asDWord(b.frame);
  // _b.unknown = "00FF00FF";
  // _b.floor_flag1 = parseFloorFlag(b.floor_flag1);
  // _b.floor_flag2 = parseFloorFlag(b.floor_flag2);
  // _b.floor_flag3 = parseFloorFlag(b.floor_flag3);
  // _b.floor_flag4 = parseFloorFlag(b.floor_flag4);
  // _b.floor_flag5 = parseFloorFlag(b.floor_flag5);
  // return _b;
  return b;
}

// const csvColumns = ['block', 'pcx_file', 'pcx_x', 'pcx_y', 'direction', 'roof_y', 'tile_sound', 'animated', 'orientation', 'main_index', 'sub_index', 'frame', 'unknown', 'floor_flag1', 'floor_flag2', 'floor_flag3', 'floor_flag4', 'floor_flag5'];
const levelsTxtColumns = ['Name', 'Id', 'Pal', 'Act', 'QuestFlag', 'QuestFlagEx', 'Layer', 'SizeX', 'SizeY', 'SizeX(N)', 'SizeY(N)', 'SizeX(H)', 'SizeY(H)', 'OffsetX', 'OffsetY', 'Depend', 'Teleport', 'Rain', 'Mud', 'NoPer', 'LOSDraw', 'FloorFilter', 'BlankScreen', 'DrawEdges', 'IsInside', 'DrlgType', 'LevelType', 'SubType', 'SubTheme', 'SubWaypoint', 'SubShrine', 'Vis0', 'Vis1', 'Vis2', 'Vis3', 'Vis4', 'Vis5', 'Vis6', 'Vis7', 'Warp0', 'Warp1', 'Warp2', 'Warp3', 'Warp4', 'Warp5', 'Warp6', 'Warp7', 'Intensity', 'Red', 'Green', 'Blue', 'Portal', 'Position', 'SaveMonsters', 'Quest', 'WarpDist', 'MonLvl1', 'MonLvl2', 'MonLvl3', 'MonLvl1Ex', 'MonLvl2Ex', 'MonLvl3Ex', 'MonDen', 'MonDen(N)', 'MonDen(H)', 'MonUMin', 'MonUMax', 'MonUMin(N)', 'MonUMax(N)', 'MonUMin(H)', 'MonUMax(H)', 'MonWndr', 'MonSpcWalk', 'NumMon', 'mon1', 'mon2', 'mon3', 'mon4', 'mon5', 'mon6', 'mon7', 'mon8', 'mon9', 'mon10', 'mon11', 'mon12', 'mon13', 'mon14', 'mon15', 'mon16', 'mon17', 'mon18', 'mon19', 'mon20', 'mon21', 'mon22', 'mon23', 'mon24', 'mon25', 'rangedspawn', 'nmon1', 'nmon2', 'nmon3', 'nmon4', 'nmon5', 'nmon6', 'nmon7', 'nmon8', 'nmon9', 'nmon10', 'nmon11', 'nmon12', 'nmon13', 'nmon14', 'nmon15', 'nmon16', 'nmon17', 'nmon18', 'nmon19', 'nmon20', 'nmon21', 'nmon22', 'nmon23', 'nmon24', 'nmon25', 'umon1', 'umon2', 'umon3', 'umon4', 'umon5', 'umon6', 'umon7', 'umon8', 'umon9', 'umon10', 'umon11', 'umon12', 'umon13', 'umon14', 'umon15', 'umon16', 'umon17', 'umon18', 'umon19', 'umon20', 'umon21', 'umon22', 'umon23', 'umon24', 'umon25', 'cmon1', 'cmon2', 'cmon3', 'cmon4', 'cpct1', 'cpct2', 'cpct3', 'cpct4', 'camt1', 'camt2', 'camt3', 'camt4', 'Themes', 'SoundEnv', 'Waypoint', 'LevelName', 'LevelWarp', 'EntryFile', 'ObjGrp0', 'ObjGrp1', 'ObjGrp2', 'ObjGrp3', 'ObjGrp4', 'ObjGrp5', 'ObjGrp6', 'ObjGrp7', 'ObjPrb0', 'ObjPrb1', 'ObjPrb2', 'ObjPrb3', 'ObjPrb4', 'ObjPrb5', 'ObjPrb6', 'ObjPrb7', 'Beta'];

export function importLevelsTxt(file: File, separator = '\t'): Promise<LevelsTxt[]> {
  return new Promise((resolve) => {
    const reader = new FileReader();
    
    reader.onload = (event) => {
      if (event.target) {
        const text = (event.target.result as string);
        const parsed = text.split('\n').map((tb) => tb.split(separator));

        // const blocks = [1, 2, 3];
        let levels: LevelsTxt[] = [];
        parsed.forEach((b) => {
          const row = ({} as LevelsTxt);
          levelsTxtColumns.forEach((key, i) => {
            (row as any)[key] = b[i];
          });
          
          levels.push(row);
        });

        // Remove "index" row
        levels.shift();

        // Remove rows 'Null' and 'Expansion'
        levels = levels.filter(l => (l['Id'] !== '' && l['Id'] !== '0'));

        const $settings = useSettingsStore();
        if ($settings.filename === '') {
          $settings.filename = removeFileExtension(file.name).filename;
        }

        resolve(levels);
      }
    }

    reader.readAsText(file);
  });
}

const difficultySizeX = ['SizeX', 'SizeX(N)', 'SizeX(H)'];
const difficultySizeY = ['SizeY', 'SizeY(N)', 'SizeY(H)'];
const difficultyMonDen = ['MonDen', 'MonDen(N)', 'MonDen(H)'];
const difficultyMonUMin = ['MonUMin', 'MonUMin(N)', 'MonUMin(H)'];
const difficultyMonUMax = ['MonUMax', 'MonUMax(N)', 'MonUMax(H)'];
export function getLevelStatsByDifficulty(level: LevelsTxt, difficulty: number) {
  return {
    sizeX: (level as any)[difficultySizeX[difficulty]],
    sizeY: (level as any)[difficultySizeY[difficulty]],
    monDen: (level as any)[difficultyMonDen[difficulty]],
    monUMin: (level as any)[difficultyMonUMin[difficulty]],
    monUMax: (level as any)[difficultyMonUMax[difficulty]],
  }
}

// const exportColumnsFromHexToDec = ['direction', 'orientation', 'main_index', 'sub_index', 'frame'];
// function exportAsCsv(blocks: BlockIni[], filename: string) {
//   const texts = [csvColumns.join(',')];
//   blocks.forEach((b) => {
//     const blockText = ([] as string[]);
//     csvColumns.forEach((k) => {
//       let v = (b as any)[k];
//       if (typeof v === 'object' && 'length' in v) {
//         v = v.join(" ");
//       }
//       if (exportColumnsFromHexToDec.includes(k)) {
//         blockText.push(`${parseInt(v, 16)}`);
//       }
//       else {
//         blockText.push(`${v}`);
//       }
//     });
//     texts.push(blockText.join(','));
//   });
//   const text = texts.join('\n');
//   const blob = new Blob([text], { type: 'text/plain' })
//   useFileDownload().fromBlob(blob, { filename: `${filename}.csv` });
//   return text;
// }
