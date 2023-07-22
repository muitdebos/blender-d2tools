/**************************
 * FCR - Faster Cast Rate *
 **************************/
function GetCastFrames(animLength, animSpeed, fcr) {
  // Hardcoded cap at 75
  const efcr = Math.min(Math.floor(fcr * 120 / (fcr + 120)), 75);
  const frames = Math.ceil(256 * animLength / Math.floor(animSpeed * (100 + efcr) / 100) - 1);
  return frames;
}

// Sorceress Lightning frames use a slightly modified calculation
function GetCastFramesLightning(animLength, animSpeed, fcr) {
  // Hardcoded cap at 75
  const efcr = Math.min(Math.floor(fcr * 120 / (fcr + 120)), 75);
  const frames = Math.ceil(256 * animLength / Math.floor(animSpeed * (100 + efcr) / 100));
  return frames;
}


function GetCastFrameBreakpoints(animLength, animSpeed, useLightningFrames = false) {
  const results = [];
  // Caps out at 200 FCR due to hardcoded cap at 75
  for (let i = 0; i <= 200; i++) {
    const cfi = useLightningFrames ? GetCastFramesLightning(animLength, animSpeed, i) : GetCastFrames(animLength, animSpeed, i);
    const previous = results[results.length - 1];
    if (previous) {
      if (previous.frames !== cfi) {
        results.push({
          fcr: i,
          frames: cfi,
        });
      }
    }
    else {
      results.push({
        fcr: i,
        frames: cfi,
      });
    }
  }
  return results;
}

/*****************************
 * FHR - Faster Hit Recovery *
 *****************************/
function GetFhrFrames(animLength, animSpeed, fhr) {
  const efhr = Math.floor(fhr * 120 / (fhr + 120));
  const frames = Math.ceil(256 * animLength / Math.floor(animSpeed * (50 + efhr) / 100) - 1);
  return frames;
}

function GetFhrBreakpoints(animLength, animSpeed) {
  const results = [];
  for (let i = 0; i <= 400; i++) {
    const fhri = GetFhrFrames(animLength, animSpeed, i);
    const previous = results[results.length - 1];
    if (previous) {
      if (previous.frames !== fhri) {
        results.push({
          fhr: i,
          frames: fhri,
        });
      }
    }
    else {
      results.push({
        fhr: i,
        frames: fhri,
      });
    }
  }
  return results;
}

/*******************************
 * FBR - Faster Block Recovery *
 *******************************/
function GetFbrFrames(animLength, animSpeed, fbr) {
  const efbr = Math.floor(fbr * 120 / (fbr + 120));
  const frames = Math.ceil(256 * animLength / Math.floor(animSpeed * (50 + efbr) / 100) - 1);
  return frames;
}

function GetFbrFramesHolyShield(animLength, animSpeed, fbr) {
  const efbr = Math.floor(fbr * 120 / (fbr + 120)) + 50;
  const frames = Math.ceil(256 * animLength / Math.floor(animSpeed * (50 + efbr) / 100) - 1);
  return frames;
}

function GetFbrBreakpoints(animLength, animSpeed, useHolyShield = false) {
  const results = [];
  for (let i = 0; i <= 400; i++) {
    const fbri = useHolyShield ? GetFbrFramesHolyShield(animLength, animSpeed, i) : GetFbrFrames(animLength, animSpeed, i);
    const previous = results[results.length - 1];
    if (previous) {
      if (previous.frames !== fbri) {
        results.push({
          fbr: i,
          frames: fbri,
        });
      }
    }
    else {
      results.push({
        fbr: i,
        frames: fbri,
      });
    }
  }
  return results;
}