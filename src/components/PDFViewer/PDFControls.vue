<template>
  <div class="page-controls">
    <button
      type="button"
      class="button-left"
      title="Page down"
      :disabled="page <= 1"
      @click="emit('page-down')"
    >
      <ChevronLeftIcon />
    </button>
    <div class="controller">
      <input
        ref="inputField"
        class="input-field"
        :value="page"
        @input="onPageChanged"
        @blur="onBlur"
      >
      <span> of {{ numOfPages }}</span>
    </div>
    <button
      type="button"
      class="button-right button_page-up"
      title="Page up"
      :disabled="page >= numOfPages"
      @click="emit('page-up')"
    >
      <ChevronRightIcon />
    </button>

    <div class="pdf-zoom">
      <button
        type="button"
        class="icon button-left"
        title="Zoom in"
        :disabled="scale > 5"
        @click.prevent.stop="zoomIn"
      >
        <ZoomInIcon />
      </button>
      <button
        type="button"
        class="icon"
        title="Zoom out"
        :disabled="scale < 1.05"
        @click.prevent.stop="zoomOut"
      >
        <ZoomOutIcon />
      </button>
      <button
        type="button"
        class="icon"
        title="Fit width"
        @click.prevent.stop="fitWidth"
      >
        <ExpandIcon />
      </button>
      <button
        type="button"
        class="icon button-right"
        title="Fit auto"
        @click.prevent.stop="fitAuto"
      >
        <ShrinkIcon />
      </button>
    </div>
  </div>
</template>

<script setup>
import ChevronLeftIcon from '../../assets/chevron-left.svg'
import ChevronRightIcon from '../../assets/chevron-right.svg'
import ZoomInIcon from '../../assets/zoom-in.svg'
import ZoomOutIcon from '../../assets/zoom-out.svg'
import ExpandIcon from '../../assets/expand.svg'
import ShrinkIcon from '../../assets/shrink.svg'

const props = defineProps({
  page: {
    type: Number,
    required: true,
  },
  numOfPages: {
    type: Number,
    required: true,
  },
  scale: {
    type: Number,
    required: true,
  },
  increment: {
    type: Number,
    required: true,
  },
  isDisabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'page-up',
  'page-down',
  'change-page',
  'change-scale',
  'fit',
])

function onPageChanged(e) {
  const value = e.target.value.trim()
  if (value.length === 0) return
  if (Number.isNaN(+value) || +value <= 0) {
    e.target.value = 1
    emit('change-page', 1)
  } else if (value > props.numOfPages) {
    e.target.value = props.numOfPages
    emit('change-page', props.numOfPages)
  } else {
    emit('change-page', +value)
  }
}

function onBlur(e) {
  e.target.value = props.page
}

function updateScale(scale) {
  emit('change-scale', { newScale: scale })
}

function zoomIn() {
  updateScale(props.scale + props.increment)
}

function zoomOut() {
  if (props.scale <= props.increment) return
  updateScale(props.scale - props.increment)
}

function fitWidth() {
  emit('fit', 'width')
}
function fitAuto() {
  emit('fit', 'auto')
}
</script>

<style lang="scss" scoped>
.page-controls {
  position: absolute;
  display: flex;
  z-index: 40;
  align-items: center;
  bottom: 5%;
  left: 50%;
  background: white;
  transform: translateX(-50%);
  transition: opacity ease-in-out 0.2s;
  box-shadow: 0 30px 40px 0 rgba(16, 36, 94, 0.2);
  border-radius: 4px;
  font-family: sans-serif;

 .input-field {
    width: 1.5rem;
    text-align: center;
  }

  button {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    background: white;
    border: 0;
    border-radius: 4px;
    transition: all 0.2s ease-in;

    svg {
      width: 1.1rem;
      height: 1.1rem;
      color: #4b5563;
    }

    &:hover:not([disabled]) {
      background-color: #efeeee;
    }
    &:active {
      transform: scale(0.95);
    }
    &:disabled svg {
      color: #e6e6e6;
    }

    &.button-left {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
    }

    &.button-right {
      border-top-left-radius: 0;
      border-bottom-left-radius: 0;
    }
  }
}
.controller {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.2rem;
  margin-right: 0.2rem;
}

span {
  font-size: 0.75rem;
  padding: 0 0.5rem;
  white-space: nowrap;
}

.pdf-zoom {
  display: flex;
  height: 40px;
  align-items: center;
  justify-items: center;

  .icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    pointer: cursor;

    svg {
      width: 1.1rem;
      height: 1.1rem;
      color: #4b5563;
    }
  }
}
</style>
