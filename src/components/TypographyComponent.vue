<template>
    <div class="absolute inset-0 grid place-items-center" v-if="loading">
        <div class="flex items-center justify-center font-mono tracking-wider">
            <span class="pr-2">Loading</span>
            <i class="animate-spin icon-dl-loading"></i>
        </div>
    </div>
    <dl-typography
        v-else
        :variant="isMarkdown ? 'div' : 'pre'"
        :markdown="isMarkdown"
    >
        {{ text }}
    </dl-typography>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { DlTypography } from '@dataloop-ai/components'

const getFileExtension = (url: string) => url.split('.').pop()

export default defineComponent({
    name: 'TypographyComponent',
    components: {
        DlTypography
    },
    props: {
        url: {
            type: String,
            required: true
        }
    },
    setup(props) {
        const loading = ref(true)
        const text = ref(null)
        const fileExtension = getFileExtension(props.url)
        const isMarkdown = fileExtension.toLowerCase().trim() === 'md'

        onMounted(async () => {
            await fetch(props.url)
                .then((response) => response.text())
                .then((data) => {
                    text.value = data
                })
                .catch((error) =>
                    console.error('Error fetching the file: ', error)
                )

            loading.value = false
        })

        return {
            text,
            loading,
            fileExtension,
            isMarkdown
        }
    }
})
</script>

<style lang="scss">
body {
    @apply overflow-y-auto h-screen;
}
</style>
