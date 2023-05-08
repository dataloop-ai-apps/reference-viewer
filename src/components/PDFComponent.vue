<template>
  <iframe
    id="pdf-js-viewer"
    title="webviewer"
    frameborder="0"
    :src="`/pdfjs-3.6.172-dist/web/viewer.html?file=${url}`"
    :width="width"
    :height="height"
  ></iframe>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

defineProps({
  url: {
    type: String,
    required: true,
  },
})

const width = ref(window.innerWidth)
const height = ref(window.innerHeight)

const onResize = () => {
  width.value = window.innerWidth
  height.value = window.innerHeight
}

onMounted(() => {
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
})
</script>
