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
          class="pr-6"
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
          />
          <v-card
            v-for="note in pinNotes"
            :key="note.id"
            :value="note"
            :class="{'pin-note': true, hidden: !note.showNote || !note.inBounds }"
            :style="{'top': `${note.notePositionY}px`, 'left': `${note.notePositionX}px`}"
          >
            {{ note.note }}
          </v-card>
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

.pin-note {
  position: absolute;
  max-width: 300px;
  padding: 2px;
  background-color: white;
  border: 1px solid black;
}

.hidden {
  display: none;
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
import { getNonTiledImage, postGisToPoint } from '../utilities/utiltyFunctions';
import store, { TiffFrame } from '../store';
import DatasetSubimageSelector from '../components/DatasetSubimageSelector.vue';
import InvestigationSidebar from '../components/InvestigationSidebar.vue';
import InvestigationDetailFrameMenu from '../components/InvestigationDetailFrameMenu.vue';
import { Dataset, Pin } from '../generatedTypes/AtlascopeTypes';
import type { DatasetEmbedding } from '../generatedTypes/AtlascopeTypes';

interface RootDatasetEmbedding {
  id: null;
  child_bounding_box: number[];
  parent: null;
  child: number;
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

interface PinNote extends Pin {
  showNote: boolean;
  inBounds: boolean;
  notePositionX: number;
  notePositionY: number;
}

interface BandSpec {
  frame: number;
  palette: string;
}

interface TileLayerStyleDict {
  bands: BandSpec[];
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
      zoomLevel,
      xCoord,
      yCoord,
    } = useGeoJS(map);
    const loaded = ref(false);
    const sidebarCollapsed = ref(true);
    const hoverText = ref('');

    function toggleSidebar() {
      sidebarCollapsed.value = !sidebarCollapsed.value;
    }

    const selectedDataset: Ref<Dataset | null> = ref(null);
    const rootDataset = computed(() => store.state.rootDataset);
    const tilesourceDatasets = computed(() => store.getters.tilesourceDatasets);
    const selectionMode = computed(() => store.state.selectionMode);
    /* eslint-disable */
    let selectionLayer: any;
    let featureLayer: any;
    let pinFeature: any;
    let nonTiledOverlayFeature: any;
    const rootDatasetLayer: Ref<any> = ref(null);
    /* eslint-enable */
    const pinNotes: Ref<PinNote[]> = ref([]);
    const frames: Ref<TiffFrame[]> = computed(() => store.state.rootDatasetFrames);

    function rootDatasetChanged(newRootDataset: Dataset) {
      selectedDataset.value = newRootDataset;
      store.dispatch.updateSelectedPins([]);
      store.dispatch.setRootDataset(newRootDataset);
    }

    function selectPinsForRootDataset() {
      store.dispatch.updateSelectedPins(store.state.currentPins.filter(
        (pin: Pin) => pin.parent === rootDataset.value?.id,
      ));
    }

    function getSelectedFrameStyle(): BandSpec[] {
      return frames.value.filter((frame: TiffFrame) => frame.displayed).map((frame: TiffFrame) => ({
        frame: frame.frame,
        palette: `${frame.color}`,
      }));
    }

    function buildUrlQueryArgs() {
      const style: TileLayerStyleDict = {
        bands: getSelectedFrameStyle(),
      };
      const encodedStyle = encodeURIComponent(JSON.stringify(style));
      return `?style=${encodedStyle}`;
    }

    function tearDownMap() {
      exit();
      selectionLayer = null;
      featureLayer = null;
      pinFeature = null;
    }

    function movePinNoteCards() {
      if (!featureLayer || !pinFeature || !map.value) { return; }
      pinFeature.data().forEach((pin: Pin) => {
        const { x, y } = postGisToPoint(pin.child_location) || { x: 0, y: 0 };
        const newScreenCoords = pinFeature.featureGcsToDisplay({ x, y });
        const note = pinNotes.value.find((pinNote) => pinNote.id === pin.id);
        if (note) {
          const {
            left, top, width, height,
          } = map.value?.getBoundingClientRect() || {
            left: 0, top: 0, width: 0, height: 0,
          };
          note.notePositionX = newScreenCoords.x + left;
          note.notePositionY = newScreenCoords.y + top;
          if (note.notePositionX > left + width
              || note.notePositionY > top + height
              || note.notePositionX < left
              || note.notePositionY < top
              || zoomLevel.value < (pin.minimum_zoom || 0)
              || zoomLevel.value > (pin.maximum_zoom || 40)) {
            note.inBounds = false;
          } else {
            note.inBounds = true;
          }
        }
      });
    }

    function showHidePinsForZoomLevel(level: number) {
      if (pinFeature) {
        pinFeature.style('fillOpacity', (pin: Pin) => (
          (level >= (pin.minimum_zoom || 0) && level <= (pin.maximum_zoom || 40)) ? 0.8 : 0));
        pinFeature.style('strokeOpacity', (pin: Pin) => (
          (level >= (pin.minimum_zoom || 0) && level <= (pin.maximum_zoom || 40)) ? 0.8 : 0));
        pinFeature.draw();
      }
    }

    watch([xCoord, yCoord, zoomLevel], () => {
      showHidePinsForZoomLevel(zoomLevel.value);
      movePinNoteCards();
    });

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
        url: `${apiRoot}/datasets/tile_source/${rootDatasetID}/tiles/{z}/{x}/{y}.png`,
        crossDomain: 'use-credentials',
      };
      createMap(mapParams);
      rootDatasetLayer.value = createLayer('osm', rootLayerParams);

      const visited: Set<RootDatasetEmbedding | DatasetEmbedding> = new Set();
      const stack: Array<StackFrame> = [];
      /* eslint-disable */
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
        /* eslint-enable */
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
            url: `${apiRoot}/datasets/tile_source/${datasetID}/tiles/{z}/{x}/{y}.png`,
            crossDomain: 'use-credentials',
          };
          createLayer(
            'osm',
            layerParams,
            `+proj=longlat +axis=enu +xoff=-${offset.x} +yoff=${
              offset.y
            } +s11=${1 / scale} +s22=${1 / scale}`,
          );

          /* eslint-disable */
          const frontier = embeddings.filter((e) => e.parent === datasetID);
          stack.unshift(
            ...frontier.map((e) => ({
              embedding: e,
              parent: { scale, offset },
              treeDepth: treeDepth + 1,
            })),
          );
          /* eslint-enable */
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
        const newUrl = `${apiRoot}/datasets/tile_source/${rootDataset.value.id}/tiles/{z}/{x}/{y}.png${queryString}`;
        rootDatasetLayer.value.url(newUrl).draw();
      }
    }, { deep: true });

    function handleSelectionChange() {
      const annotations = selectionLayer.annotations();
      /* eslint-disable-next-line */
      annotations.forEach((annotation: any) => {
        annotation.style({
          fillColor: '#00796b',
          strokeColor: '#00796b',
        });
        if (annotation.state() !== geoAnnotations.state.create) {
          if (annotations.length > 1) {
            selectionLayer.removeAnnotation(annotation);
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
      if (!selectionLayer) {
        selectionLayer = createLayer('annotation', {
          annotations: ['rectangle'],
          showLabels: false,
        });
        selectionLayer.geoOn(geoEvents.annotation.add, handleSelectionChange);
        selectionLayer.geoOn(geoEvents.annotation.update, handleSelectionChange);
        selectionLayer.geoOn(geoEvents.annotation.remove, handleSelectionChange);
        selectionLayer.geoOn(geoEvents.annotation.state, handleSelectionChange);
      }
      if (!selectionMode.value) {
        selectionLayer.mode(null);
        selectionLayer.removeAllAnnotations();
        store.commit.setSubimageSelection(null);
      } else {
        selectionLayer.mode('rectangle');
      }
    });

    const selectedPins: Ref<Pin[]> = computed(() => store.state.selectedPins);
    /**
     * Create note cards for any pins without a child dataset.
     */
    function createPinNotes() {
      const noteOnlyPins = store.state.currentPins.filter(
        (pin: Pin) => (!pin.child && pin.note?.length),
      );
      pinNotes.value = noteOnlyPins.map((pin) => ({
        ...pin,
        showNote: false,
        inBounds: pin.minimum_zoom === 0,
        notePositionX: 0,
        notePositionY: 0,
      }));
    }

    async function toggleNonTiledImageOverlay(pin: Pin, dataset: Dataset) {
      if (!dataset.content) return;
      if (!featureLayer) return; // sanity check. this should exist
      if (!nonTiledOverlayFeature) {
        nonTiledOverlayFeature = featureLayer.createFeature('quad');
      }
      const quadData = nonTiledOverlayFeature.data() || [];
      // eslint-disable-next-line
      const existingOverlay = quadData.find((overlay: any) => overlay.pinId === pin.id);
      if (existingOverlay) {
        nonTiledOverlayFeature.data(
          // eslint-disable-next-line
          nonTiledOverlayFeature.data().filter((overlay: any) => overlay.pinId !== pin.id),
        ).draw();
        nonTiledOverlayFeature.draw();
      } else {
        try {
          const urlRoot = process.env.VUE_APP_API_ROOT;
          const url = `${urlRoot}/datasets/tile_source/${dataset.id}/thumbnail.png`;
          const image: HTMLImageElement = await getNonTiledImage(url);
          image.crossOrigin = 'Anonymous';
          const ul = postGisToPoint(pin.child_location) || { x: 0, y: 0 };
          const lr = { x: ul.x + (image.width || 0), y: ul.y + (image.height || 0) };
          quadData.push({
            ul,
            lr,
            image,
            pinId: pin.id,
          });
          nonTiledOverlayFeature.data(quadData).draw();
        } catch (error) {
          // eslint-disable-next-line
          console.error(`Failed to show overlay for dataset ${dataset.id}.`);
        }
      }
    }

    function toggleDatasetPin(pin: Pin) {
      const childDataset: Dataset | undefined = store.state.currentDatasets.find(
        (dataset: Dataset) => dataset.id === pin.child,
      );
      if (!childDataset) return;
      switch (childDataset.dataset_type) {
        case 'non_tiled_image':
          toggleNonTiledImageOverlay(pin, childDataset);
          break;
        default:
          break;
      }
    }

    watch(selectedPins, (newPins, oldPins) => {
      if (!featureLayer) {
        featureLayer = createLayer(
          'feature',
          { features: ['point', 'line', 'polygon', 'quad.image'] },
        );
      }
      const newPinIds = newPins.map((pin) => pin.id);
      const removedPinIds = oldPins.filter((pin: Pin) => !newPinIds.includes(pin.id))
        .map((pin: Pin) => pin.id);
      if (nonTiledOverlayFeature) {
        const overlayData = nonTiledOverlayFeature.data();
        const newOverlayData = overlayData.filter(
          (overlay: any) => !removedPinIds.includes(overlay.pinId),
        );
        nonTiledOverlayFeature.data(newOverlayData).draw();
      }
      removedPinIds.forEach((pinId) => {
        const note = pinNotes.value.find((pinNote) => pinNote.id === pinId);
        if (note) {
          note.showNote = false;
        }
      });
      if (!pinFeature) {
        /* eslint-disable */
        pinFeature = featureLayer.createFeature('point')
          .data(selectedPins.value)
          .position((pin: Pin) => (postGisToPoint(pin.child_location) || { x: 0, y: 0 }))
          .style({
            radius: 10,
            strokeColor: 'white',
            fillColor: (pin: Pin) => pin.color,
          })
          .draw();
        pinFeature.geoOn(geoEvents.feature.mouseclick, (event: any) => {
          if (!map.value) { return; }

          if (event.mouse.buttonsDown.left) {
            if (!event.data.child && event.data.note) {
              // note-only pins
              const noteToToggle = pinNotes.value.find((note) => note.id === event.data.id);
              if (noteToToggle) {
                noteToToggle.showNote = !noteToToggle.showNote;
                noteToToggle.notePositionX = event.mouse.page.x;
                noteToToggle.notePositionY = event.mouse.page.y;
              }
            } else if (event.data.child) {
              // pins with child dataset
              toggleDatasetPin(event.data);
            }
          }
        });
      } else {
        pinFeature.data(selectedPins.value).draw();
      }
      showHidePinsForZoomLevel(zoomLevel.value);
      /* eslint-enable */
    });

    onMounted(async () => {
      await store.dispatch.fetchCurrentInvestigation(props.investigation);
      selectedDataset.value = store.state.rootDataset;
      drawMap(store.state.rootDataset);
      createPinNotes();
      selectPinsForRootDataset();
      loaded.value = true;
    });

    return {
      loaded,
      sidebarCollapsed,
      hoverText,
      toggleSidebar,
      map,
      tilesourceDatasets,
      rootDataset,
      selectedDataset,
      rootDatasetChanged,
      selectedPins,
      pinNotes,
    };
  },
});
</script>
