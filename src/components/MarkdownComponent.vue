<template>
    <div class="p-8 bg-[#0D1117] text-[#e6edf3]">
        <div class="flex justify-center">
            <div class="markdown-body" v-html="renderedMarkdown"></div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps({
    url: {
        type: String,
        required: true
    }
})

const renderedMarkdown = ref('')

fetch(props.url)
    .then((response) => response.text())
    .then((markdownContent) => {
        const md = new MarkdownIt({
            html: true,
            linkify: true,
            typographer: true,
            xhtmlOut: true,
            breaks: false
        })
        renderedMarkdown.value = md.render(markdownContent)
    })
    .catch((error) => console.error('Error fetching the file: ', error))
</script>

<style lang="scss">
body {
    @apply overflow-y-auto h-screen;
}
.markdown-body {
    @apply max-w-screen-lg p-8 leading-normal;

    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans',
        Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';
    word-wrap: break-word;

    h1 {
        @apply mt-6 mb-4 font-semibold;
        padding-bottom: 0.3em;
        font-size: 2em;
        border-bottom: 1px solid #21262d;
    }

    p,
    ul,
    ol {
        @apply mt-0 mb-4;
    }

    ul,
    ol {
        @apply list-disc text-[#f0f6fc];
        font-size: 1rem;
        padding-left: 2em;
    }

    a {
        @apply text-[#2f81f7] underline underline-offset-2;
    }

    hr {
        height: 0.25em;
        padding: 0;
        margin: 24px 0;
        background-color: #30363d;
        border: 0;
    }

    img {
        @apply inline-block;
    }

    kbd {
        --color-neutral-muted: rgba(110, 118, 129, 0.4);

        @apply inline-block leading-normal rounded-md;
        display: inline-block;
        padding: 3px 5px;
        font:
            11px ui-monospace,
            SFMono-Regular,
            SF Mono,
            Menlo,
            Consolas,
            Liberation Mono,
            monospace;
        color: #f0f6fc;
        vertical-align: middle;
        background-color: #161b22;
        border: solid 1px var(--color-neutral-muted);
        border-bottom-color: var(--color-neutral-muted);
        box-shadow: inset 0 -1px 0 var(--color-neutral-muted);
    }
}
</style>
