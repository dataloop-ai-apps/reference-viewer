<template>
  <div v-if="!loading && url.length" class="imageContainer">
    <img ref="imgElem" :src="url" />
  </div>
  <div v-if="!url.length" class="content">No media found</div>
</template>

<script setup lang="ts">
/* eslint-disable */
defineProps([
  'setIsOpen',
  'isBlackTheme',
  'url',
  'loading',
  'top',
  'right',
  'width',
  'height',
  'imgWidth',
  'imgHeight',
])
/* eslint-enable */
</script>

<style lang="scss">
.imageContainer {
  overflow: hidden;
  background: #2a2a2e;

  img {
    width: 100vw;
    height: 100vh;
    object-fit: contain;
  }
}

.content {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  align-self: center;
}
</style>
