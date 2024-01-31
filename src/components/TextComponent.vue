<template>
    <div class="prefer-system-theme">
        <div class="p-2 py-4 lg:py-8">
            <div class="flex justify-center text-xl">
                <pre class="whitespace-pre-wrap break-words">{{ text }}</pre>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
    url: {
        type: String,
        required: true
    }
})

const text = ref(null)
fetch(props.url)
    .then((response) => response.text())
    .then((data) => {
        text.value = data
    })
    .catch((error) => console.error('Error fetching the file: ', error))
</script>

<style lang="scss">
body {
    @apply overflow-y-auto h-screen;
}

@media (prefers-color-scheme: dark) {
    body .prefer-system-theme {
        @apply bg-[#0D1117] text-[#e6edf3];
    }
}
</style>
