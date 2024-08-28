export interface IFileDownloadConfig {
  filename?: string,
}

export function useFileDownload(): {
  fromUrl: (url: string, config?: IFileDownloadConfig) => any,
  fromBlob: (url: Blob, config?: IFileDownloadConfig) => any,
} {
  function fromUrl(url: string, config?: IFileDownloadConfig) {
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', config?.filename || 'file.zip');
    document.body.appendChild(link);
    link.click();
    link.remove();
    return link;
  }

  function fromBlob(blob: Blob, config?: IFileDownloadConfig) {
    const url = window.URL.createObjectURL(blob);
    return fromUrl(url, config);
  }

  return {
    fromUrl,
    fromBlob,
  };
}
