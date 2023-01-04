<template>
  <div class="full-screen">
    <div
      v-if="loading"
      class="content"
    >
      Content is loading...
    </div>
    <div v-else>
      <FloatingWindow
        :loading="loading"
        :type-of-content="typeOfContent"
        :set-is-open="(value) => (isOpen = value)"
        :width="initialWidth"
        :height="initialHeight"
        :url="url"
        :type="type"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import FloatingWindow from './components/FloatingWindow.vue'

defineProps({
  msg: {
    type: String,
    default: '',
  },
})

const refresh = () => window.location.reload()
const isOpen = ref(false)
const loading = ref(true)
const typeOfContent = ref('image')
const initialWidth = null
const initialHeight = null
const type = ref('image/png')
const url = ref('')

onMounted(async () => {
  await dl.init()
  dl.on('ready', async () => {
    const item = await dl.items.get()
    const previewModality = item.metadata.system.modalities.find((m) => m.type === 'preview')
    if (previewModality) {
      if (previewModality.refType === 'url') {
        url.value = previewModality.ref
      } else {
        const modalityItem = await dl.items.stream(previewModality.stream)
        url.value = modalityItem
      }
      type.value = previewModality.mimetype ? previewModality.mimetype : type.value
      typeOfContent.value = type.value
    }
    loading.value = false
  })
})
</script>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.content {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
}
</style>
