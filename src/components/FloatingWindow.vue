<template>
    <div>
        <VideoComponent
            v-if="
                (typeOfContent.includes('video') &&
                    videoHeight &&
                    videoWidth) ||
                (typeOfContent.includes('video') && width && height)
            "
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
            v-else-if="typeOfContent.includes('image')"
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
            v-else-if="typeOfContent.includes('pdf')"
            :url="url"
            :loading="loading"
        />
        <AudioComponent
            v-else-if="
                typeOfContent.includes('audio') && !loading && url.length
            "
            :url="url"
        />
        <TypographyComponent
            v-else-if="
                (typeOfContent.includes('markdown') ||
                    typeOfContent.includes('txt')) &&
                !loading &&
                url.length
            "
            :url="url"
        />
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import VideoComponent from './VideoComponent.vue'
import ImageComponent from './ImageComponent.vue'
import PDFComponent from './PDFComponent.vue'
import TypographyComponent from './TypographyComponent.vue'

export default defineComponent({
    props: [
        'setIsOpen',
        'loading',
        'isBlackTheme',
        'url',
        'top',
        'right',
        'type',
        'typeOfContent',
        'width',
        'height'
    ],
    data() {
        return {
            imgWidth: null,
            imgHeight: null,
            videoWidth: null,
            videoHeight: null
        }
    },
    mounted() {
        if (
            this.typeOfContent.includes('video') &&
            !this.width &&
            !this.height
        ) {
            const video = document.createElement('video')
            video.addEventListener('loadedmetadata', () => {
                this.videoWidth.value = video.videoWidth
                this.videoHeight.value = video.videoHeight + 100
            })
            video.src = this.url
        } else if (
            this.typeOfContent.includes('image') &&
            !this.width &&
            !this.height
        ) {
            const img = new Image()
            img.onload = () => {
                this.imgWidth.value = img.naturalWidth
                this.imgHeight.value = img.naturalHeight
            }
            img.src = this.url
        }
    }
})
</script>
