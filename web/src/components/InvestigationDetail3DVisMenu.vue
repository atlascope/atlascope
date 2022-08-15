<template>
  <v-menu
    v-model="showMenu"
    :position-x="positionx"
    :position-y="positiony + 48"
    absolute
    offset-y
    :close-on-click="false"
  >
    <v-list>
      <v-list-item
        :href="externalGlanceLink"
        target="_blank"
        @click="showMenu = false"
      >
        <v-list-item-title>
          Open with Paraview Glance
        </v-list-item-title>
      </v-list-item>
      <v-list-item>
        <v-list-item-title>
          Cancel
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
  PropType,
  computed,
  watch,
} from '@vue/composition-api';
import { Dataset } from '../generatedTypes/AtlascopeTypes';

export default defineComponent({
  props: {
    dataset: {
      type: Object as () => Dataset,
      required: false,
    },
    visible: {
      type: Boolean as PropType<boolean>,
      default: false,
    },
    positionx: {
      type: Number as PropType<number>,
      default: 0,
    },
    positiony: {
      type: Number as PropType<number>,
      default: 0,
    },
  },
  setup(props) {
    const showMenu = ref(props.visible);
    const externalGlanceLink = computed(() => {
      if (props.dataset) {
        const apiRoot = process.env.VUE_APP_API_ROOT;
        const datasetUrl = `${apiRoot}/datasets/${props.dataset.id}/download`;
        return `http://localhost:9999/?name=${props.dataset.name}&url=${datasetUrl}`;
      }
      return '';
    });
    watch(() => props.visible, () => {
      showMenu.value = props.visible;
    });
    return {
      showMenu,
      externalGlanceLink,
    };
  },
});
</script>
