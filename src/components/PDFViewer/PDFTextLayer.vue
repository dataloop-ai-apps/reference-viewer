<template>
  <div
    ref="textLayerDiv"
    class="textLayer pdf__wrapper-text-layer"
  />
</template>

<script setup>
import {
  onMounted, ref, toRaw, computed,
} from 'vue'

import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf'
import PDFJSWorker from 'pdfjs-dist/legacy/build/pdf.worker.entry'
import * as pdfjsViewer from 'pdfjs-dist/legacy/web/pdf_viewer'
import 'pdfjs-dist/legacy/web/pdf_viewer.css'

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

const textContent = ref(null)
const textLayerDiv = ref(null)

async function loadTextContent() {
  await toRaw(props.page).getTextContent()
    .then((textContentData) => {
      textContent.value = textContentData
    })
    .catch((error) => {
      throw new Error(error)
    })
}

const viewport = computed(() => {
  const { page, scale } = props

  return page.getViewport({ scale })
})

async function renderTextLayer() {
  if (!textContent.value) return null

  textLayerDiv.value.innerHTML = ''

  const pdfWrapper = document.getElementById('pdfWrapper')
  const pdfWrapperElStyles = window.getComputedStyle(pdfWrapper)
  const pdfWrapperElWidth = parseFloat(pdfWrapperElStyles.width)

  textLayerDiv.value.style.cssText = `height: ${
    toRaw(viewport.value).height
  }px; width: ${
    props.scale ? toRaw(viewport.value).width : pdfWrapperElWidth
  }px;`
  // Create new instance of TextLayerBuilder class
  const textLayer = new pdfjsViewer.TextLayerBuilder({
    textLayerDiv: textLayerDiv.value,
    pageIndex: toRaw(props.page).pageNumber - 1,
    eventBus: new pdfjsViewer.EventBus(),
    viewport: toRaw(props.viewport),
    enhanceTextSelection: true,
  })

  // Set text-fragments
  textLayer.setTextContent(textContent.value)
  // Render text-fragments
  return textLayer.render()
}

onMounted(async () => {
  await loadTextContent()
  renderTextLayer()
})

</script>

<style lang="scss">
.pdf__wrapper-text-layer {
  margin: 0 auto;

  br {
    display: none;
  }
}
</style>
