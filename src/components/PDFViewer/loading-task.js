import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf'
import PDFJSWorker from 'pdfjs-dist/legacy/build/pdf.worker.entry'

// See, https://mozilla.github.io/pdf.js/api/draft/module-pdfjsLib.html#~DocumentInitParameters
// eslint-disable-next-line import/prefer-default-export
export const createLoadingTask = (src) => {
  pdfjsLib.GlobalWorkerOptions.workerSrc = PDFJSWorker.toString()
  const loadingTask = pdfjsLib.getDocument({
    url: src,
    withCredentials: true,
  })
  return loadingTask
}
