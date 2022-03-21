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
          v-if="!loaded || tilesourceDatasets.length > 0"
          v-model="selectedDataset"
          class="atlascope-dataset-select"
          :items="tilesourceDatasets"
          item-text="name"
          item-value="id"
          return-object
          single-line
          dense
          hide-details
          @change="activeDatasetChanged"
        />
        <v-banner
          v-if="loaded && tilesourceDatasets.length === 0"
          single-line
        >
          <v-icon left>
            mdi-alert
          </v-icon>
          No tilesource datasets found for this investigation.
        </v-banner>
        <v-spacer />
      </v-col>
      <v-col v-if="frameInfo.length > 0">
        <v-menu
          v-model="showFrames"
          :close-on-content-click="false"
          offset-y
          max-height="500px"
        >
          <template
            v-slot:activator="{ on, attrs }"
          >
            <v-btn
              color="blue"
              dark
              v-bind="attrs"
              v-on="on"
            >
              Frames
            </v-btn>
          </template>
          <v-card>
            <v-card-text>
              <v-list>
                <v-list-item
                  v-for="frame in frameInfo"
                  :key="frame.frame"
                  :value="frame"
                >
                  <v-list-item-action>
                    <v-switch
                      v-model="frame.displayed"
                    />
                  </v-list-item-action>
                  <v-list-item>
                    <div class="frame-row ma-0 pa-0">
                      <v-text-field
                        v-model="frame.color"
                        :hint="frame.name"
                        persistent-hint
                        maxlength="6"
                      />
                    </div>
                  </v-list-item>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="primary"
                text
                @click="updateFrameInfo"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-col>
    </v-row>
    <v-row class="ma-0 pa-0">
      <v-col class="ma-0 pa-0">
        <v-sheet height="85vh">
          <div
            ref="map"
            class="map"
          >
            <v-menu
              v-model="showNote"
              :position-x="noteX"
              :position-y="noteY"
              absolute
              offset-y
              allow-overflow
            >
              <v-card class="pin-hover-card">
                {{ hoverText }}
              </v-card>
            </v-menu>
          </div>
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

.pin-hover-card {
  width: 500px;
}

.frame-row {
  display: inline;
}
</style>

<script lang="ts">
import {
  ref, defineComponent, onMounted, PropType, computed, watch, Ref,
} from '@vue/composition-api';
import useGeoJS from '../utilities/useGeoJS';
import { Point, postGisToPoint } from '../utilities/utiltyFunctions';
import store from '../store';
import InvestigationSidebar from '../components/InvestigationSidebar.vue';
import { Dataset, Pin } from '../generatedTypes/AtlascopeTypes';

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
    const map: Ref<null | HTMLElement> = ref(null);
    const {
      clampBoundsX,
      exit,
      generatePixelCoordinateParams,
      createMap,
      createLayer,
      geoEvents,
    } = useGeoJS(map);
    const loaded = ref(false);
    const sidebarCollapsed = ref(true);
    const showNote = ref(false);
    const noteX = ref(0);
    const noteY = ref(0);
    const hoverText = ref('');

    function toggleSidebar() {
      sidebarCollapsed.value = !sidebarCollapsed.value;
    }

    const selectedDataset: Ref<Dataset | null> = ref(null);
    const activeDataset = computed(() => store.state.activeDataset);
    const activeDatasetMetadata = computed(() => store.state.activeDatasetMetadata);
    const tilesourceDatasets = computed(() => store.getters.tilesourceDatasets);
    /* eslint-disable */
    let featureLayer: any;
    let pinFeature: any;
    /* eslint-enable */
    const frameInfo: Ref<any[]> = ref([]);
    const showFrames: Ref<boolean> = ref(false);
    const activeDatasetLayer: Ref<any> = ref(null);

    function activeDatasetChanged(newActiveDataset: Dataset) {
      selectedDataset.value = newActiveDataset;
      store.dispatch.updateSelectedPins([]);
      store.dispatch.setActiveDataset(newActiveDataset);
    }

    function buildUrlQueryArgs() {
      const channels: number[] = [];
      const colors: string[] = [];
      const selectedFrames = frameInfo.value.filter((frame) => frame.displayed);
      if (selectedFrames.length === 0) {
        return '';
      }
      selectedFrames.forEach((frame) => {
        channels.push(frame.frame);
        colors.push(frame.color);
      });
      return `?channels=${channels.join(',')}&colors=${colors.join(',')}`;
    }

    function updateFrameInfo() {
      showFrames.value = false;
      if (activeDataset.value && activeDatasetLayer.value) {
        const apiRoot = process.env.VUE_APP_API_ROOT;
        const newUrl = `${apiRoot}/datasets/${activeDataset.value.id}/tiles/{z}/{x}/{y}.png${buildUrlQueryArgs()}`;
        activeDatasetLayer.value.url(newUrl).draw();
      }
    }

    function tearDownMap() {
      exit();
      featureLayer = null;
      pinFeature = null;
    }

    function drawMap(dataset: Dataset | null) {
      tearDownMap();
      if (!dataset || !dataset.id) {
        return;
      }
      const tileSourceMetadata = store.state.datasetTileMetadata[dataset.id];
      if (!tileSourceMetadata) {
        return;
      }
      if (tileSourceMetadata.additional_metadata.frames) {
        frameInfo.value = tileSourceMetadata.additional_metadata.frames.map((frame) => ({
          name: frame.Name || 'no name',
          frame: frame.Frame,
          displayed: true,
          color: '000000',
        }));
      }
      const geojsParams = generatePixelCoordinateParams(
        tileSourceMetadata.size_x || 0,
        tileSourceMetadata.size_y || 0,
        tileSourceMetadata.tile_size || 0,
        tileSourceMetadata.tile_size || 0,
      );
      if (!geojsParams || !geojsParams.map || !geojsParams.layer) {
        return;
      }
      const apiRoot = process.env.VUE_APP_API_ROOT;
      const queryString = buildUrlQueryArgs();
      geojsParams.layer.url = `${apiRoot}/datasets/${dataset.id}/tiles/{z}/{x}/{y}.png${queryString}`;
      geojsParams.layer.crossDomain = 'use-credentials';

      createMap(geojsParams.map);
      activeDatasetLayer.value = createLayer('osm', geojsParams.layer);
      clampBoundsX(false);
    }

    watch(activeDataset, (newValue) => {
      drawMap(newValue);
    });

    const selectedPins: Ref<Pin[]> = computed(() => store.state.selectedPins);
    function getPinsToDisplay() {
      // TODO: as we move towards embedding multiple datasets into the view,
      // we will need a more sophisticated way to determine which pins to render
      // and determining where they should be rendered
      const selectedPinsForActiveDataset = selectedPins.value.filter(
        (pin) => pin.parent === activeDataset.value?.id,
      );
      const pinFeatureData = selectedPinsForActiveDataset.map((pin) => {
        const location: Point = postGisToPoint(pin.child_location) || { x: 0, y: 0 };
        return {
          ...location,
          id: pin.id,
          color: pin.color,
          note: pin.note,
        };
      });
      return pinFeatureData;
    }

    watch(selectedPins, () => {
      if (!featureLayer) {
        featureLayer = createLayer('feature', { features: ['point', 'line', 'polygon'] });
      }
      const pinFeatureData = getPinsToDisplay();
      if (!pinFeature) {
        /* eslint-disable */
        pinFeature = featureLayer.createFeature('point')
          .data(pinFeatureData)
          .position((pin: any) => ({ x: pin.x, y: pin.y }))
          .style({
            radius: 10,
            strokeColor: 'white',
            fillColor: (pin: any) => pin.color,
          })
          .draw();
        pinFeature.geoOn(geoEvents.feature.mouseon, (event: any) => {
          if (!map.value) { return; }
          showNote.value = true;
          noteX.value = event.mouse.page.x;
          noteY.value = event.mouse.page.y;
          hoverText.value = event.data.note;
        });
        pinFeature.geoOn(geoEvents.feature.mouseoff, (event: any) => {
          if (!map.value) { return; }
          showNote.value = false;
          hoverText.value = '';
        });
      } else {
        pinFeature.data(pinFeatureData).draw();
      }
      /* eslint-enable */
    });

    onMounted(async () => {
      await store.dispatch.fetchCurrentInvestigation(props.investigation);
      selectedDataset.value = store.state.activeDataset;
      drawMap(store.state.activeDataset);
      loaded.value = true;
    });

    return {
      loaded,
      sidebarCollapsed,
      showNote,
      noteX,
      noteY,
      hoverText,
      toggleSidebar,
      map,
      tilesourceDatasets,
      activeDataset,
      activeDatasetMetadata,
      selectedDataset,
      activeDatasetChanged,
      updateFrameInfo,
      showFrames,
      frameInfo,
      selectedPins,
    };
  },
});
</script>
