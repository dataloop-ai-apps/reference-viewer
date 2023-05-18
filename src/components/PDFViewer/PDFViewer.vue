<template>
  <div class="relative flex flex-col h-screen">
    <PDFNavbar
      :title="getFilenameFromUrl(url)"
      :num-pages="pdf?.numPages"
      :show-sidebar="showSidebar"
      :page-scale-value="pageScaleValue"
      :page-zoom="pageZoom"
      @on-toggle-sidebar="toggleSidebar"
      @on-page-prev="toRaw(pdfViewer)?.previousPage()"
      @on-page-next="toRaw(pdfViewer)?.nextPage()"
      @on-zoom-in="zoomIn"
      @on-zoom-out="zoomOut"
      @on-page-scale-change="setPageScale"
    />
    <PDFDocument
      v-if="pdf"
      :show-sidebar="showSidebar"
      :page-scale-value="pageScaleValue"
      @on-pdf-viewer-set="setPdfViewer"
    />
    <div
      v-else
      class="font-thin text-2xl text-center text-gray-800 h-40 m-auto"
    >
      Loading...
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, provide, ref, toRaw } from 'vue'

import * as pdfjs from 'pdfjs-dist'
import { type PDFDocumentProxy, getFilenameFromUrl } from 'pdfjs-dist'

import {
  type PDFViewer,
  EventBus,
  PDFLinkService,
  PDFFindController,
} from 'pdfjs-dist/web/pdf_viewer'

const props = defineProps({
  url: {
    type: String,
    required: true,
  },
})

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`

const pageScaleValue = ref('page-width')
const pageZoom = ref(1)
const pdf = ref<PDFDocumentProxy | null>(null)
const showSidebar = ref(true)
const pdfViewer = ref<PDFViewer>(null)

const setPdfViewer = (viewer: PDFViewer) => {
  pdfViewer.value = viewer
}

const setPageScale = (fit: string) => {
  pageScaleValue.value = fit
}

const zoomIn = () => {
  if (!pdfViewer.value.currentScaleValue)
    toRaw(pdfViewer.value).currentScaleValue = 'page-width'
  toRaw(pdfViewer.value)?.increaseScale()
}

const zoomOut = () => {
  if (!pdfViewer.value.currentScaleValue)
    toRaw(pdfViewer.value).currentScaleValue = 'page-width'
  toRaw(pdfViewer.value)?.decreaseScale()
}

const eventBus = new EventBus()
const pdfLinkService = new PDFLinkService({ eventBus })
const pdfFindController = new PDFFindController({
  eventBus,
  linkService: pdfLinkService,
})

provide('pdf', pdf)
provide('eventBus', eventBus)
provide('pdfLinkService', pdfLinkService)
provide('pdfFindController', pdfFindController)

onMounted(async () => {
  const loadingTask = pdfjs.getDocument({
    url: props.url,
    cMapUrl: `https://unpkg.com/pdfjs-dist@${pdfjs.version}/cmaps/`,
    cMapPacked: true,
    enableXfa: true,
  })
  loadingTask.promise.then(function (pdfDoc: PDFDocumentProxy) {
    pdf.value = pdfDoc

    eventBus.on('scalechanging', ({ scale }) => {
      pageZoom.value = scale
    })
  })
})

const toggleSidebar = () => (showSidebar.value = !showSidebar.value)
</script>