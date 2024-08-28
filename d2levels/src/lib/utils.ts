export function zp(src: string, pad: number, cutoff?: boolean) {
  if (src.length > pad && !cutoff) { return src; }
  return `${"0".repeat(pad || 2)}${src}`.slice(-1 * (pad || 2));
}

export function dec2hex(decimal: number): string {
  return decimal.toString(16);
}

export function hex2dec(hex: string): number {
  return parseInt(hex, 16);
}

export function arrmove(arr: any[], from: number, to: number) {
  arr.splice(to, 0, arr.splice(from, 1)[0]);
  return arr;
}

export function removeFileExtension(filename: string) {
  const splits = filename.split('.');
  if (splits.length > 1) {
    const extension = splits.pop();
    return {
      filename: splits.join('.'),
      extension: extension || '',
    }
  }
  return {
    filename: filename,
    extension: '',
  }
}