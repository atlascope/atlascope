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
          @change="rootDatasetChanged"
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
      <v-col cols="auto">
        <investigation-detail-frame-menu />
      </v-col>
      <v-col cols="auto">
        <dataset-subimage-selector />
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
  ref,
  defineComponent,
  onMounted,
  PropType,
  computed,
  watch,
  Ref,
} from '@vue/composition-api';
import useGeoJS from '../utilities/useGeoJS';
import { Point, postGisToPoint } from '../utilities/utiltyFunctions';
import store from '../store';
import DatasetSubimageSelector from '../components/DatasetSubimageSelector.vue';
import InvestigationSidebar from '../components/InvestigationSidebar.vue';
import InvestigationDetailFrameMenu from '../components/InvestigationDetailFrameMenu.vue';
import { Dataset, Pin } from '../generatedTypes/AtlascopeTypes';
import type { DatasetEmbedding } from '../generatedTypes/AtlascopeTypes';

interface RootDatasetEmbedding {
  id: null;
  child_bounding_box: number[];
  parent: null;
  child: string;
}

interface StackFrame {
  embedding: DatasetEmbedding | RootDatasetEmbedding;
  parent: {
    scale: number;
    offset: {
      x: number;
      y: number;
    };
  };
  treeDepth: number;
}

export default defineComponent({
  name: 'InvestigationDetail',

  components: {
    InvestigationSidebar,
    InvestigationDetailFrameMenu,
    DatasetSubimageSelector,
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
      geoAnnotations,
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
    const rootDataset = computed(() => store.state.rootDataset);
    const tilesourceDatasets = computed(() => store.getters.tilesourceDatasets);
    const selectionMode = computed(() => store.state.selectionMode);
    /* eslint-disable */
    let annotationLayer: any;
    let featureLayer: any;
    let pinFeature: any;
    const rootDatasetLayer: Ref<any> = ref(null);
    const frames = computed(() => store.state.rootDatasetFrames);
    /* eslint-enable */

    function rootDatasetChanged(newRootDataset: Dataset) {
      selectedDataset.value = newRootDataset;
      store.dispatch.updateSelectedPins([]);
      store.dispatch.setRootDataset(newRootDataset);
    }

    function buildUrlQueryArgs() {
      const channels: number[] = [];
      const colors: string[] = [];
      const selectedFrames = frames.value.filter((frame) => frame.displayed);
      if (selectedFrames.length === 0) {
        return '';
      }
      selectedFrames.forEach((frame) => {
        channels.push(frame.frame);
        colors.push(frame.color);
      });
      return `?channels=${channels.join(',')}&colors=${colors.join(',')}`;
    }

    function tearDownMap() {
      exit();
      annotationLayer = null;
      featureLayer = null;
      pinFeature = null;
    }

    function drawMap(dataset: Dataset | null) {
      tearDownMap();
      if (!dataset || !dataset.id) {
        return;
      }

      const apiRoot = process.env.VUE_APP_API_ROOT;
      const embeddings = store.state.datasetEmbeddings;
      const rootDatasetID = dataset.id;
      const rootTileMetadata = store.state.datasetTileMetadata[rootDatasetID];

      if (
        rootTileMetadata === undefined
        || rootTileMetadata.size_x === undefined
        || rootTileMetadata.size_y === undefined
        || rootTileMetadata.tile_size === undefined
        || rootTileMetadata.levels === undefined
      ) {
        return;
      }

      const rootPixelParams = generatePixelCoordinateParams(
        rootTileMetadata.size_x || 0,
        rootTileMetadata.size_y || 0,
        rootTileMetadata.tile_size || 0,
        rootTileMetadata.tile_size || 0,
      );
      const mapParams = {
        ...rootPixelParams.map,
        max: 40,
      };
      const rootLayerParams = {
        ...rootPixelParams.layer,
        zIndex: 0,
        url: `${apiRoot}/datasets/${rootDatasetID}/tiles/{z}/{x}/{y}.png`,
        crossDomain: 'use-credentials',
      };
      createMap(mapParams);
      rootDatasetLayer.value = createLayer('osm', rootLayerParams);

      const visited: Set<RootDatasetEmbedding | DatasetEmbedding> = new Set();
      const stack: Array<StackFrame> = [];
      stack.unshift(
        ...embeddings
          .filter((e) => e.parent === rootDatasetID)
          .map((e) => ({
            embedding: e,
            parent: { scale: 1, offset: { x: 0, y: 0 } },
            treeDepth: 1,
          })),
      );

      while (stack.length > 0) {
        const { embedding, parent, treeDepth } = stack.shift()!;
        if (!visited.has(embedding)) {
          visited.add(embedding);

          if (
            embedding === undefined
            || embedding.child_bounding_box === undefined
            || embedding.child_bounding_box.length !== 4
          ) {
            return;
          }

          const datasetID = embedding.child;
          const tileMetadata = store.state.datasetTileMetadata[datasetID];

          if (
            tileMetadata === undefined
            || tileMetadata.size_x === undefined
            || tileMetadata.size_y === undefined
            || tileMetadata.tile_size === undefined
            || tileMetadata.levels === undefined
          ) {
            return;
          }

          const boundingBox = {
            x: {
              min: embedding.child_bounding_box[0],
              max: embedding.child_bounding_box[2],
            },
            y: {
              min: embedding.child_bounding_box[1],
              max: embedding.child_bounding_box[3],
            },
          };
          const scale = Math.min(
            (parent.scale * (boundingBox.x.max - boundingBox.x.min))
              / tileMetadata.size_x,
            (parent.scale * (boundingBox.y.max - boundingBox.y.min))
              / tileMetadata.size_y,
          );
          const offset = {
            x: (parent.scale / scale) * (parent.offset.x + boundingBox.x.min),
            y: (parent.scale / scale) * (parent.offset.y + boundingBox.y.min),
          };
          const pixelParams = generatePixelCoordinateParams(
            tileMetadata.size_x || 0,
            tileMetadata.size_y || 0,
            tileMetadata.tile_size || 0,
            tileMetadata.tile_size || 0,
          );
          const layerParams = {
            ...pixelParams.layer,
            zIndex: treeDepth,
            url: `${apiRoot}/datasets/${datasetID}/tiles/{z}/{x}/{y}.png`,
            crossDomain: 'use-credentials',
          };
          createLayer(
            'osm',
            layerParams,
            `+proj=longlat +axis=enu +xoff=-${offset.x} +yoff=${
              offset.y
            } +s11=${1 / scale} +s22=${1 / scale}`,
          );

          const frontier = embeddings.filter((e) => e.parent === datasetID);
          stack.unshift(
            ...frontier.map((e) => ({
              embedding: e,
              parent: { scale, offset },
              treeDepth: treeDepth + 1,
            })),
          );
        }
      }
      clampBoundsX(false);
    }

    watch(rootDataset, (newValue) => {
      drawMap(newValue);
    });

    watch(frames, () => {
      if (rootDataset.value && rootDatasetLayer) {
        const queryString = buildUrlQueryArgs();
        const apiRoot = process.env.VUE_APP_API_ROOT;
        const newUrl = `${apiRoot}/datasets/${rootDataset.value.id}/tiles/{z}/{x}/{y}.png${queryString}`;
        rootDatasetLayer.value.url(newUrl).draw();
      }
    }, { deep: true });

    function handleSelectionChange() {
      const annotations = annotationLayer.annotations();
      /* eslint-disable-next-line */
      annotations.forEach((annotation: any) => {
        annotation.style({
          fillColor: '#00796b',
          strokeColor: '#00796b',
        });
        if (annotation.state() !== geoAnnotations.state.create) {
          if (annotations.length > 1) {
            annotationLayer.removeAnnotation(annotation);
          } else {
            const corners = annotation.coordinates();
            const newSelection = [
              corners[1].x, corners[1].y, corners[3].x, corners[3].y,
            ].map(
              (num) => Math.round(num),
            );
            store.commit.setSubimageSelection(newSelection);
          }
        }
      });
    }

    watch(selectionMode, () => {
      if (!annotationLayer) {
        annotationLayer = createLayer('annotation', {
          annotations: ['rectangle'],
          showLabels: false,
        });
        annotationLayer.geoOn(geoEvents.annotation.add, handleSelectionChange);
        annotationLayer.geoOn(geoEvents.annotation.update, handleSelectionChange);
        annotationLayer.geoOn(geoEvents.annotation.remove, handleSelectionChange);
        annotationLayer.geoOn(geoEvents.annotation.state, handleSelectionChange);
      }
      if (!selectionMode.value) {
        annotationLayer.mode(null);
        annotationLayer.removeAllAnnotations();
        store.commit.setSubimageSelection(null);
      } else {
        annotationLayer.mode('rectangle');
      }
    });

    const selectedPins: Ref<Pin[]> = computed(() => store.state.selectedPins);
    function getPinsToDisplay() {
      // TODO: as we move towards embedding multiple datasets into the view,
      // we will need a more sophisticated way to determine which pins to render
      // and determining where they should be rendered
      const selectedPinsForRootDataset = selectedPins.value.filter(
        (pin) => pin.parent === rootDataset.value?.id,
      );
      const pinFeatureData = selectedPinsForRootDataset.map((pin) => {
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
      selectedDataset.value = store.state.rootDataset;
      drawMap(store.state.rootDataset);
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
      rootDataset,
      selectedDataset,
      rootDatasetChanged,
      selectedPins,
    };
  },
});
</script>
