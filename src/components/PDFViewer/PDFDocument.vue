<template>
  <section
    class="overflow-hidden flex-1 bg-[#f1f5f9] grid transition-all duration-75 ease-in"
    :style="{ 'grid-template-columns': `${showSidebar ? '8rem' : '0rem'} 1fr` }"
  >
    <Suspense>
      <PDFSidebar
        class="transition-all duration-75 ease-in-out"
        :class="{ opacity: +showSidebar }"
      />
    </Suspense>
    <div class="relative box-content">
      <div id="viewerContainer" ref="containerRef">
        <div id="viewer" class="pdfViewer"></div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { inject, onBeforeUnmount, onMounted, ref, toRaw, watch } from 'vue'
import {
  type EventBus,
  PDFViewer,
  type PDFLinkService,
} from 'pdfjs-dist/web/pdf_viewer'
import { PDFDocumentProxy } from 'pdfjs-dist'

const emit = defineEmits(['on-pdf-viewer-set'])
const props = defineProps({
  showSidebar: Boolean,
  pageScaleValue: {
    type: String,
    required: true,
  },
})

const pdf: PDFDocumentProxy = inject('pdf')
const eventBus: EventBus = inject('eventBus')
const pdfLinkService: PDFLinkService = inject('pdfLinkService')
const pdfFindController = inject('pdfFindController')

const containerRef = ref<HTMLDivElement>(null)
const pdfViewer = ref(null)
watch(
  () => props.pageScaleValue,
  (newValue) => {
    toRaw(pdfViewer.value).currentScaleValue = newValue
  }
)

const resizePdf = () => {
  toRaw(pdfViewer.value).currentScaleValue = props.pageScaleValue
  toRaw(pdfViewer.value).update()
}

onMounted(() => {
  window.addEventListener('resize', resizePdf)

  pdfViewer.value = new PDFViewer({
    container: containerRef.value,
    eventBus,
    linkService: pdfLinkService,
    findController: pdfFindController,
  })
  pdfViewer.value.container = containerRef.value

  toRaw(pdfLinkService).setViewer(toRaw(pdfViewer.value))

  toRaw(pdfViewer.value).setDocument(toRaw(pdf.value))
  toRaw(pdfLinkService).setDocument(toRaw(pdf.value), null)
  emit('on-pdf-viewer-set', toRaw(pdfViewer.value))
})

onBeforeUnmount(() => window.removeEventListener('resize', resizePdf))
</script>

<style lang="scss">
#viewerContainer {
  @apply absolute overflow-auto inset-0 outline-0;

  #viewer {
    @apply relative w-fit mx-auto;
  }

  .page {
    box-sizing: content-box;
    direction: ltr;
    margin: 0 auto;
    position: relative;
    overflow: visible;
    border: 9px solid transparent;
    background-clip: content-box;
    background-color: rgba(255, 255, 255, 1);

    /* Copyright 2014 Mozilla Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

    --highlight-bg-color: rgb(180, 0, 170, 1);
    --highlight-selected-bg-color: rgb(0, 100, 0, 1);

    @media screen and (forced-colors: active) {
      --highlight-bg-color: Highlight;
      --highlight-selected-bg-color: ButtonText;
    }

    [data-main-rotation='90'] {
      transform: rotate(90deg) translateY(-100%);
    }

    [data-main-rotation='180'] {
      transform: rotate(180deg) translate(-100%, -100%);
    }

    [data-main-rotation='270'] {
      transform: rotate(270deg) translateX(-100%);
    }

    .textLayer {
      position: absolute;
      inset: 0;
      z-index: 2;
      overflow: hidden;
      opacity: 0.2;
      line-height: 1;
      text-align: initial;
      transform-origin: 0 0;
      text-size-adjust: none;
      forced-color-adjust: none;
    }

    .textLayer span,
    .textLayer br {
      position: absolute;
      color: transparent;
      white-space: pre;
      transform-origin: 0% 0%;
      cursor: text;
    }

    /* Only necessary in Google Chrome, see issue 14205, and most unfortunately
 * the problem doesn't show up in "text" reference tests. */
    .textLayer span.markedContent {
      top: 0;
      height: 0;
    }

    .textLayer .highlight {
      margin: -1px;
      padding: 1px;
      background-color: var(--highlight-bg-color);
      border-radius: 4px;
    }

    .textLayer .highlight.appended {
      position: initial;
    }

    .textLayer .highlight.begin {
      border-radius: 4px 0 0 4px;
    }

    .textLayer .highlight.end {
      border-radius: 0 4px 4px 0;
    }

    .textLayer .highlight.middle {
      border-radius: 0;
    }

    .textLayer .highlight.selected {
      background-color: var(--highlight-selected-bg-color);
    }

    /* Avoids https://github.com/mozilla/pdf.js/issues/13840 in Chrome */
    .textLayer br::selection {
      background: transparent;
    }

    .textLayer .endOfContent {
      position: absolute;
      inset: 100% 0 0;
      z-index: -1;
      display: block;
      cursor: default;
      user-select: none;
    }

    .textLayer .endOfContent.active {
      top: 0;
    }
  }
}
</style>
