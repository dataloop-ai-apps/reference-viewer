<template>
  <div>
    <VideoComponent
      v-if="typeOfContent.includes('video') && videoHeight && videoWidth || typeOfContent.includes('video') && width && height"
      :set-is-open="setIsOpen"
      :is-black-theme="isBlackTheme"
      :url="url"
      :top="top"
      :right="right"
      :type="type"
      :width="width"
      :height="height"
      :video-width="videoWidth"
      :video-height="videoHeight"
    />
    <ImageComponent
      v-if="typeOfContent.includes('image')"
      :set-is-open="setIsOpen"
      :loading="loading"
      :url="url"
      :top="top"
      :right="right"
      :width="width"
      :height="height"
      :img-width="imgWidth"
      :img-height="imgHeight"
    />
    <PDFComponent
      v-if="typeOfContent.includes('pdf')"
      :url="url"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import VideoComponent from './VideoComponent.vue'
import ImageComponent from './ImageComponent.vue'
import PDFComponent from './PDFComponent.vue'

const props = defineProps({
  setIsOpen: {
    type: Function,
    default: () => ({}),
  },
  loading: {
    type: Boolean,
  },
  isBlackTheme: {
    type: Boolean,
  },
  url: {
    type: String,
    default: '',
  },
  top: {
    type: String,
    default: '',
  },
  right: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: '',
  },
  typeOfContent: {
    type: String,
    default: '',
  },
  width: {
    type: String,
    default: '',
  },
  height: {
    type: String,
    default: '',
  },
})

const imgWidth = ref(null)
const imgHeight = ref(null)
const videoWidth = ref(null)
const videoHeight = ref(null)

onMounted(() => {
  if (props.typeOfContent === 'video' && !props.width && !props.height) {
    const video = document.createElement('video')
    video.src = props.url
    video.addEventListener('loadedmetadata', () => {
      videoWidth.value = video.videoWidth
      videoHeight.value = video.videoHeight + 100
    })
  } else if (props.typeOfContent === 'image' && !props.width && !props.height) {
    const img = new Image()
    img.src = props.url
    img.addEventListener('load', () => {
      imgWidth.value = img.naturalWidth
      imgHeight.value = img.naturalHeight
    })
  }
})

</script>
