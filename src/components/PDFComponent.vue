<script lang="ts">
import { defineComponent, onMounted, reactive, ref } from "vue";
import VuePdf from "./PDFViewer/vue-pdf.vue";
import { createLoadingTask } from "./PDFViewer/loading-task";
import { VuePdfPropsType } from "./PDFViewer/vue-pdf-props"; // Prop type definitions can also be imported
import { PDFDocumentProxy } from "pdfjs-dist/types/src/display/api";

// import ZoomInIcon from "../assets/icon-zoom-in.svg";
// import ZoomOutIcon from "../assets/icon-zoom-out.svg";
// import ExpandIcon from "../assets/icon-expand.svg";
// import ShrinkIcon from "../assets/icon-shrink.svg";

export default defineComponent({
  name: "PDFComponent",
  components: { VuePdf },
  props: ["url"],
  data() {
    return {
      page: 1,
    };
  },
  setup(props) {
    const pdfSrc = ref<VuePdfPropsType["src"]>(
      props.url
    );
    const numOfPages = ref(0);

    onMounted(() => {
      const loadingTask = createLoadingTask(pdfSrc.value.toString());
      loadingTask.promise.then((pdf: PDFDocumentProxy) => {
        numOfPages.value = pdf.numPages;
      });
    });
    return {
      pdfSrc,
      numOfPages,
    };
  },

  computed: {
    isDisabled() {
      return !this.scale;
    },
  },
  methods: {
    zoomIn() {},
    zoomOut() {},
    fitWidth() {},
    fitAuto() {},
    pageUp() {
      this.page < this.numOfPages ? this.page++ : 1;

      this.goToPage();
    },
    pageDown() {
      this.page > 1 ? this.page-- : 1;

      this.goToPage();
    },
    goToPage(p = this.page) {
      if (
        window.pageYOffset <= this.findPos(document.getElementById(p)) ||
        (document.getElementById(p + 1) &&
          window.pageYOffset >= this.findPos(document.getElementById(p + 1)))
      ) {
        // window.scrollTo(0,this.findPos(document.getElementById(p)));
        document.getElementById(p).scrollIntoView();
      }
    },
    findPos(obj) {
      return obj.offsetTop;
    },
    onPageChanged(e) {
      const value = e.target.value.trim();

      if (value.length === 0 || isNaN(+value) || value < 1) {
        e.target.value = 1;
        this.page = 1;
      } else if (value > this.numOfPages) {
        e.target.value = this.numOfPages;
        this.page = this.numOfPages;
      } else {
        this.page = e.target.value;
      }
      this.goToPage(this.page);
    },
    onScrollPageChanged(page: number) {
      this.page = page;
    },
  },
});
</script>

<template>
  <div id="pdf-document" class="pdf-document">
    <div class="render-block scrolling-document" style="">
      <VuePdf
        v-for="i in numOfPages"
        :key="i"
        :src="pdfSrc"
        :page="i"
        class="scrolling-page"
        @onScrollPageChanged="onScrollPageChanged"
      />
    </div>
  </div>
  <div class="page-controls">
    <button type="button" @click="pageDown">&lt;</button>
    <div>
      <input
        ref="inputField"
        class="input-field"
        :value="page"
        @input="onPageChanged"
      />
      <span> of {{ numOfPages }}</span>
    </div>
    <button type="button" @click="pageUp">&gt;</button>

    <!-- <div class="pdf-zoom">
      <a @click.prevent.stop="zoomIn" class="icon" :disabled="isDisabled"
        >zoomIn</a
      >
      <a @click.prevent.stop="zoomOut" class="icon" :disabled="isDisabled"
        >zoomOut</a
      >
      <a @click.prevent.stop="fitWidth" class="icon" :disabled="isDisabled"
        >fitWidth</a
      >
      <a @click.prevent.stop="fitAuto" class="icon" :disabled="isDisabled"
        >fitAuto</a
      >
    </div> -->
  </div>
</template>

<style>
.pdf-document {
  position: absolute;
  overflow: auto;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: #525f69;
}

.scrolling-document {
  width: 85%;
  margin: 0 auto;
}

.scrolling-page:first-child {
  margin-top: 1em;
}
.scrolling-page {
  margin-bottom: 0.1em;
}

.page-controls {
  position: absolute;
  display: flex;
  align-items: center;
  bottom: 5%;
  left: 50%;
  background: white;
  /* opacity: 0; */
  transform: translateX(-50%);
  transition: opacity ease-in-out 0.2s;
  box-shadow: 0 30px 40px 0 rgba(16, 36, 94, 0.2);
  border-radius: 4px;
}

.page-controls .input-field {
  width: 1.2rem;
  text-align: center;
}

.page-controls button:first-child {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.page-controls button:hover {
  background-color: #e6e6e6;
}

.page-controls button:last-child {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.page-controls button {
  width: 44px;
  height: 44px;
  background: white;
  border: 0;
  border-radius: 4px;
}

.page-controls span {
  font-size: 0.8em;
  padding: 0 0.5em;
}
</style>
