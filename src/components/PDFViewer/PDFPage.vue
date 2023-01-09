<template>
  <div
    :id="page.pageNumber"
    ref="parentWrapperRef"
    class="pdf-main"
  >
    <div
      id="pdfWrapper"
      ref="pdfWrapperRef"
      class="pdf"
    >
      <div
        :id="`pdf-page-${page.pageNumber}`"
        class="pdf__wrapper"
      >
        <canvas
          ref="canvasRef"
          v-bind="canvasAttrs"
        />
        <PDFAnnotationLayer
          v-if="props.enableAnnotations && viewport"
          :page="page"
          :viewport="viewport"
        />
        <PDFTextLayer
          v-if="props.enableTextSelection && viewport"
          :page="page"
          :viewport="viewport"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  toRaw,
  computed,
  inject,
  onMounted,
  onBeforeUnmount,
} from 'vue'

import { PIXEL_RATIO } from './utils/constants'

import PDFTextLayer from './PDFTextLayer.vue'
import PDFAnnotationLayer from './PDFAnnotationLayer.vue'

const props = defineProps({
  page: {
    type: Object,
    required: true,
  },
  scale: {
    type: Number,
    required: true,
  },
  optimalScale: {
    type: Number,
    required: true,
  },
  enableTextSelection: {
    type: Boolean,
  },
  enableAnnotations: {
    type: Boolean,
  },
})

const viewport = ref(null)
const loading = ref(false)

const parentWrapperRef = ref(null)
const pdfWrapperRef = ref(null)
const canvasRef = ref(null)

const context = ref(null)
const observer = inject('observer')

const actualSizeViewport = computed(() => viewport.value.clone({ scale: props.scale }))
const canvasStyle = computed(() => {
  const { width: actualSizeWidth, height: actualSizeHeight } = actualSizeViewport.value
  const [pixelWidth, pixelHeight] = [actualSizeWidth, actualSizeHeight]
    .map((dim) => Math.ceil(dim / PIXEL_RATIO))
  return `width: ${pixelWidth}px; height: ${pixelHeight}px;`
})
const canvasAttrs = computed(() => {
  let { width, height } = viewport.value;
  [width, height] = [width, height].map((dim) => Math.ceil(dim))
  const style = canvasStyle.value
  return {
    width,
    height,
    style,
    class: 'pdf-page box-shadow',
  }
})

viewport.value = toRaw(props.page).getViewport({ scale: props.optimalScale })

function renderPage() {
  // PDFPageProxy#render
  // Render text layer for text selection
  // https://mozilla.github.io/pdf.js/api/draft/module-pdfjsLib-PDFPageProxy.html
  toRaw(props.page).render({ canvasContext: context.value, viewport: viewport.value }).promise
    .then(() => {
      loading.value = false
    })
}

/* eslint-disable no-param-reassign */
async function scaleCanvas() {
  const canvas = canvasRef.value
  const pdfWrapperElStyles = window.getComputedStyle(pdfWrapperRef.value)
  const pdfWrapperElWidth = parseFloat(pdfWrapperElStyles.width)

  // determine the 'backing store ratio' of the canvas context
  const backingStoreRatio = context.value.webkitBackingStorePixelRatio
        || context.value.mozBackingStorePixelRatio
        || context.value.msBackingStorePixelRatio
        || context.value.oBackingStorePixelRatio
        || context.value.backingStorePixelRatio
        || 1

  // determine the actual ratio we want to draw at
  const ratio = PIXEL_RATIO / backingStoreRatio

  if (PIXEL_RATIO !== backingStoreRatio) {
    // set the 'real' canvas size to the higher width/height
    canvas.width = props.scale
      ? viewport.value.width * ratio
      : pdfWrapperElWidth * ratio
    canvas.height = viewport.value.height * ratio

    // ...then scale it back down with CSS
    canvas.style.width = props.scale ? '' : '100%'
    canvas.style.height = `${viewport.value.height}px`
  } else {
    // this is a normal 1:1 device; just scale it simply
    canvas.width = props.scale ? viewport.value.width : pdfWrapperElWidth
    canvas.height = viewport.value.height
    canvas.style.width = ''
    canvas.style.height = ''
  }
  // scale the drawing context so everything will work at the higher ratio
  await context.value.scale(ratio, ratio)

  // Draw it on the canvas
  if (context.value) {
    renderPage(pdfWrapperElWidth)
  }
}

function drawPage() {
  const canvas = canvasRef.value
  context.value = canvas.getContext('2d')
  scaleCanvas()
}

onMounted(() => {
  drawPage()
  observer.value.observe(parentWrapperRef.value)
})

onBeforeUnmount(() => {
  if (!props.page) return
  props.page.cleanup()
})
</script>

<style lang="scss">
.pdf__wrapper {
  position: relative;

  .pdf-page {
    display: block;
    margin: 0 auto;
  }

  .box-shadow {
    -webkit-box-shadow: 0 15px 30px 0 rgba(0,0,0,.11),0 5px 15px 0 rgba(0,0,0,.08);
    box-shadow: 0 15px 30px 0 rgba(0,0,0,.11),0 5px 15px 0 rgba(0,0,0,.08);
  }
}
</style>
