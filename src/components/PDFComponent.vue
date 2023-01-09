<template>
  <PDFViewer :url="url" />
</template>

<script setup>
import PDFViewer from './PDFViewer/PDFViewer.vue'

defineProps({
  url: {
    type: String,
    required: true,
  },
})

</script>

<style>
</style>
