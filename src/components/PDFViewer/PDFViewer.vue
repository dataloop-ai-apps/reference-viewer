<template>
  <div>
    <div
      id="pdf-document"
      ref="pdfRef"
      class="pdf-document"
    >
      <div
        class="scrolling-document"
        style=""
      >
        <PDFPage
          v-for="(pdfPage, i) in pages"
          :key="i"
          :page="pdfPage"
          :scale="scale"
          :optimal-scale="optimalScale"
          :fit="fit"
          class="scrolling-page"
          @change-page="changePage"
        />
      </div>
    </div>
    <PDFControls
      :page="page"
      :num-of-pages="numOfPages"
      :scale="scale"
      :increment="increment"
      @page-up="pageUp"
      @page-down="pageDown"
      @change-page="changeAndGoToPage"
      @change-scale="updateScale"
      @fit="updateFit"
    />
  </div>
</template>

<script setup>
import {
  onMounted,
  ref,
  toRaw,
  watch,
  computed,
  provide,
} from 'vue'
import { createLoadingTask } from './loading-task'
import PDFPage from './PDFPage.vue'
import PDFControls from './PDFControls.vue'

import { floor, range } from './utils/helper'
import { PIXEL_RATIO, VIEWPORT_RATIO } from './utils/constants'

const props = defineProps({
  url: {
    type: String,
    required: true,
  },
  increment: {
    type: Number,
    default: 0.25,
  },
})

const pdfSrc = ref(props.url)
const page = ref(1)
const numOfPages = ref(0)
const thePDF = ref(null)
const pages = ref([])
const fit = ref(undefined)
const scale = ref(1)
const optimalScale = ref(1)
const pdfRef = ref(null)
const timerId = ref(null)

const defaultViewport = computed(() => {
  if (!pages.value.length) return { width: 0, height: 0 }
  return pages.value[0].getViewport({ scale: 1.0 })
})

function getPages(pdf, first, last) {
  const allPages = range(first, last + 1).map((number) => toRaw(pdf).getPage(number))
  return Promise.all(allPages)
}

function findPos(obj) {
  return obj.offsetTop
}

function goToPage(p = page.value) {
  if (
    window.pageYOffset <= findPos(document.getElementById(p))
      || (document.getElementById(p + 1)
        && window.pageYOffset >= findPos(document.getElementById(p + 1)))
  ) {
    document.getElementById(p).scrollIntoView()
  }
}

function pageUp() {
  page.value < numOfPages.value ? page.value++ : 1
  goToPage()
}

function pageDown() {
  page.value > 1 ? page.value-- : 1

  goToPage()
}

function changePage(newPage) {
  page.value = newPage
}

function changeAndGoToPage(newPage) {
  changePage(newPage)
  goToPage(newPage)
}

function updateScale({ newScale, isOptimal = false }) {
  const roundedScale = floor(newScale, 2)
  if (isOptimal) optimalScale.value = roundedScale
  scale.value = roundedScale
}

function updateFit(newFit) {
  fit.value = newFit
}

function pageWidthScale() {
  if (!defaultViewport.value.width) return 0
  return ((pdfRef.value.clientWidth * PIXEL_RATIO)
    * VIEWPORT_RATIO) / defaultViewport.value.width
}

function pageHeightScale() {
  if (!defaultViewport.value.height) return 0
  return ((pdfRef.value.clientHeight * PIXEL_RATIO)
    * VIEWPORT_RATIO) / defaultViewport.value.height
}

// Determine an ideal scale using viewport of document's first page,
// the pixel ratio from the browser
// and a subjective scale factor based on the screen size.
function fitWidth() {
  const newScale = pageWidthScale()
  updateScale({ newScale, isOptimal: !optimalScale.value })
}

function fitAuto() {
  const newScale = Math.min(pageWidthScale(), pageHeightScale())
  updateScale({ newScale })
}

const options = {
  rootMargin: '5px',
  threshold: 0.5,
}

const callback = (entries, _) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      changePage(+entry.target.id)
    }
    // entry.target.classList.add( 'some-class' );
  })
}
const observer = ref(new IntersectionObserver(callback, options))
provide('observer', observer)

watch(fit, (newFit) => {
  switch (newFit) {
    case 'width':
      fitWidth()
      break
    case 'auto':
      fitAuto()
      break
    default:
      break
  }
})

function onResize() {
  fitAuto()
}

onMounted(async () => {
  const loadingTask = createLoadingTask(pdfSrc.value.toString())
  await loadingTask.promise.then((pdf) => {
    thePDF.value = pdf
    numOfPages.value = pdf.numPages
  })

  window.addEventListener('resize', () => {
    clearTimeout(timerId.value)
    timerId.value = setTimeout(onResize, 500)
  })

  await getPages(thePDF.value, 1, numOfPages.value)
    .then((pagesResult) => {
      pages.value = pagesResult
    })
    .catch((response) => {
      throw new Error(response)
    })

  fitAuto()
})
</script>

<style>
.pdf-document {
  position: absolute;
  overflow: auto;
  width: 100%;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: #2a2a2e;
}

.scrolling-page {
  margin-top: 1em;
  margin-bottom: 1em;
}

@media print {
  .pdf-document {
    position: static;
  }
}
</style>
