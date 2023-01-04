<template>
  <div
    ref="annotationLayer"
    class="pdf__wrapper-annotation-layer"
  />
</template>

<script setup>
import {
  ref, toRaw, computed, onMounted,
} from 'vue'

import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf'
import PDFJSWorker from 'pdfjs-dist/legacy/build/pdf.worker.entry'
import * as pdfjsViewer from 'pdfjs-dist/legacy/web/pdf_viewer'
import 'pdfjs-dist/legacy/web/pdf_viewer.css'

const annotations = ref(null)
const annotationLayer = ref(null)

const props = defineProps({
  page: {
    type: Object,
    required: true,
  },
  viewport: {
    type: Object,
    required: true,
  },
})

async function loadAnnotations() {
  await toRaw(props.page).getAnnotations()
    .then((annotationData) => {
      annotations.value = annotationData
    })
    .catch((error) => {
      throw new Error(error)
    })
}

const viewport = computed(() => {
  const { page, scale } = props

  return page.getViewport({ scale })
})

async function renderAnnotations() {
  if (!annotations.value) return null

  annotationLayer.value.innerHTML = ''

  const linkService = new pdfjsViewer.PDFLinkService()
  const parameters = {
    viewport: toRaw(props.viewport).clone({ dontFlip: true }),
    div: annotationLayer.value,
    annotations: toRaw(annotations.value),
    page: toRaw(props.page),
    linkService,
    downloadManager: '',
    renderInteractiveForms: false,
  }

  // Render annotation layer for clickable links
  const pdfWrapper = document.getElementById('pdfWrapper')
  const pdfWrapperElStyles = window.getComputedStyle(pdfWrapper)
  const pdfWrapperElWidth = parseFloat(pdfWrapperElStyles.width)
  annotationLayer.value.style.cssText = `height: ${
    viewport.value.height
  }px; width: ${
    props.scale ? viewport.value.width : pdfWrapperElWidth
  }px;`

  // Render the annotation layer
  return pdfjsLib.AnnotationLayer.render({
    parameters,
  })
}

onMounted(async () => {
  await loadAnnotations()
  renderAnnotations()
})

</script>

<style lang="scss">
.pdf__wrapper-annotation-layer {
  position: absolute;
  margin: 0 auto;
  left: 0;
  top: 0;
  right: 0;

  .linkAnnotation {
    position: absolute;
    z-index: 1;

    a {
      width: 100%;
      height: 100%;
      display: block;

      &:hover {
        opacity: 0.2;
        background: rgba(255, 255, 0, 1);
        box-shadow: 0 2px 10px rgba(255, 255, 0, 1);
      }
    }
  }
}
</style>
