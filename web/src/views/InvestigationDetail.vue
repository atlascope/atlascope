<template>
  <v-container
    class="grey lighten-3 pa-0 ma-0"
    fluid
    fill-height
  >
    <v-row class="ma-2 pa-0">
      <v-col
        class="ma-0 pa-0"
        cols="auto"
      >
        <v-select
          v-model="activeDataset"
          class="atlascope-dataset-select"
          :items="datasets"
          item-text="name"
          item-value="id"
          return-object
          single-line
          dense
          hide-details
          @change="activeDatasetChanged"
        />
      </v-col>
    </v-row>
    <v-row class="ma-0 pa-0">
      <v-col class="ma-0 pa-0">
        <v-sheet height="85vh">
          <div
            ref="map"
            class="map"
          />
        </v-sheet>
      </v-col>
      <v-col
        cols="auto"
        class="ma-0 pa-0"
      >
        <v-sheet
          height="85vh"
          color="teal"
        >
          <v-btn
            icon
            @click.stop="toggleSidebar"
          >
            <v-icon v-if="sidebarCollapsed">
              mdi-chevron-left
            </v-icon>
            <v-icon v-else>
              mdi-chevron-right
            </v-icon>
          </v-btn>
          <investigation-sidebar v-if="!sidebarCollapsed" />
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.map {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
}
</style>

<script lang="ts">
import {
  ref, defineComponent, onMounted, PropType, computed, Ref,
} from '@vue/composition-api';
import useGeoJS from '../utilities/useGeoJS';
import store from '../store';
import InvestigationSidebar from '../components/InvestigationSidebar.vue';
import { Dataset } from '../generatedTypes/AtlascopeTypes';

export default defineComponent({
  name: 'InvestigationDetail',

  components: {
    InvestigationSidebar,
  },

  props: {
    investigation: {
      type: String as PropType<string>,
      required: true,
    },
  },

  setup(props) {
    const map = ref(null);
    const sidebarCollapsed = ref(true);
    const activeDataset: Ref<Dataset | null> = ref(null);
    const { updateBaseLayerDataset } = useGeoJS(map);
    const mainViews = ['context', 'connections'];

    const investigationDetail = computed(() => store.state.currentInvestigation);
    const datasets = computed(() => store.state.currentDatasets);

    function toggleSidebar() {
      sidebarCollapsed.value = !sidebarCollapsed.value;
    }

    function activeDatasetChanged(newActiveDataset: Dataset) {
      store.dispatch.setActiveDataset(newActiveDataset);
    }

    onMounted(async () => {
      await store.dispatch.fetchCurrentInvestigation(props.investigation);
      activeDataset.value = store.state.activeDataset;
      if (store?.state.activeDataset?.id) {
        updateBaseLayerDataset(store.state.activeDataset.id);
      }
    });
    return {
      map,
      datasets,
      mainViews,
      sidebarCollapsed,
      toggleSidebar,
      investigationDetail,
      activeDataset,
      activeDatasetChanged,
    };
  },
});
</script>
