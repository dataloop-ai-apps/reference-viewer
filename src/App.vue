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

// const count = ref(0)

// const refresh = () => window.location.reload()

const isOpen = ref(false)
const loading = ref(true)
const typeOfContent = ref('image')
const initialWidth = null
const initialHeight = null
const type = ref('image/png')
const url = ref('')

// const log = () => console.log("hii")

onMounted(async () => {
  window.me = loading
  loading.value = false
  type.value = 'pdf'

  let item = ''
  const TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqQTVPRVF3Umpnek9ESXdNa1E1UmpjMU5VVXpRMFJGTXpsRE9URTBOMEZGUVVZMk0wWkJPQSJ9.eyJodHRwczovL2RhdGFsb29wLmFpL2F1dGhvcml6YXRpb24iOnsiZ3JvdXBzIjpbXSwicm9sZXMiOltdLCJ1c2VyX3R5cGUiOiJodW1hbiJ9LCJnaXZlbl9uYW1lIjoiRGVsbCIsImZhbWlseV9uYW1lIjoiWFBTIiwibmlja25hbWUiOiJhbGlldl9hbWlyemhhbmkiLCJuYW1lIjoiRGVsbCBYUFMiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUVkRlRwN1RBS3cza0NrUVJpMVc4VTRYOFVXTkZhR0NXQVN4SVdNZVZ0UjA1Zz1zOTYtYyIsImxvY2FsZSI6InJ1IiwidXBkYXRlZF9hdCI6IjIwMjMtMDEtMDJUMjA6MDI6MzQuMzUzWiIsImVtYWlsIjoiYWxpZXZfYW1pcnpoYW5pQG1haWwucnUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9kYXRhbG9vcC1wcm9kdWN0aW9uLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMDkyNzIwNjk1MzMyMDEwNTU3NiIsImF1ZCI6IkZyRzBIWmdhMUNLNVVWVVNKSnVEa1NEcUl0UGllV0dXIiwiaWF0IjoxNjcyNzc1ODg3LCJleHAiOjE2NzI4NjIyODd9.COj-ixNQcIGuph6L-0gxcvHlSDhGM7H8dWjnb0U7TJ_fOVtkOBITjnr3lcgfZ76CQzsePWmUmqUBFu0o9LnlOkSLOzaNrdohQ5npMB2PG_e-5kniNRW5liVszmxAYEyifzcIjmLA3hPb9HN1sNj2rtah2v8zVwYnWY0QYTzlZcA1jUP7d6FcoFhuhz6T_IAbeMmtoZ-hPot2v9lIAViByQxhBYeo6gAuQEqyXeLTqq3PEdIOMXI3po0bP6-GXk5lAvdBEv2bzY8e1kXzMrqB0mkqBYwJv8TOpfoDHlcpf9Z3JamME9v5fcQMHnW1KYrdzxyHH-JtUE3zzA57F-gKEg'
  await fetch('/api/v1/items/63b4888fa414d60f36e2a64a', {
    headers: {
      'Content-Type': 'application/json;charset=UTF-8',
      'Access-Control-Allow-Origin': '*',
      Authorization: TOKEN,
    },
  })
    .then((resp) => resp.json())
    .then((resp) => (item = resp))
  // // await dl.init()
  // // dl.on('ready', async () => {
  // // const item = await dl.items.get()
  // console.log(`item fetched -`, { item })
  const previewModality = item.metadata.system.modalities.find(
    (m) => m.type === 'preview',
  )
  if (previewModality) {
    if (true || previewModality.refType === 'url') {
      url.value = previewModality.ref
      type.value = previewModality.mimetype
    } else {
      const modalityItem = await dl.items.stream(previewModality.stream)
      url.value = modalityItem
      // type.value = modalityItem.metadata?.system?.mimetype
      // const width = modalityItem.metadata.system.width
      // const height = modalityItem.metadata.system.height
      // await dl.app.updateSlotSettings({ width, height })
    }
    typeOfContent.value = type.value.split('/')[0]
  }
  loading.value = false
  url.value = `/api/v1/items/${item.id}/stream`
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
