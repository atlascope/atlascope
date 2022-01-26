import {
  ref, onMounted, Ref, watch, computed,
} from '@vue/composition-api';

import geo from 'geojs';
import store from '../store';

export default function useGeoJS(element: Ref<HTMLElement | null>) {
  const map: Ref<any> = ref(null);
  const zoomLevel = ref(0);
  const xCoord = ref(0);
  const yCoord = ref(0);
  const activeDataset = computed(() => store.state.activeDataset);

  onMounted(() => {
    // `element.value` should always be an `HTMLElement` (not `null`)
    // by the time `onMounted` is called. However, it will be `null`
    // before that since the DOM isn't available at call time.

    // check if valid DOM element is passed.
    if (element.value !== null) {
      map.value = geo.map({ node: element.value });
      zoomLevel.value = map.value.zoom();
    }
  });

  const center = (x: number, y: number) => {
    if (map.value !== null) {
      map.value.center({ x, y });
      xCoord.value = x;
      yCoord.value = y;
    }
  };

  const zoom = (level: number) => {
    if (map.value !== null) {
      map.value.zoom(level);
      zoomLevel.value = level;
    }
  };

  const updateBaseLayerDataset = async (datasetId: string) => {
    const tileSourceMetadata = await store.dispatch.fetchDatasetMetadata(datasetId);
    if (!tileSourceMetadata) {
      return;
    }

    // Destroy this map
    map.value.exit();
    const geojsParams = geo.util.pixelCoordinateParams(
      element.value,
      tileSourceMetadata.size_x,
      tileSourceMetadata.size_y,
      tileSourceMetadata.tile_size,
      tileSourceMetadata.tile_size,
    );
    const apiRoot = process.env.VUE_APP_API_ROOT;
    geojsParams.layer.url = `${apiRoot}/datasets/${datasetId}/tiles/{z}/{x}/{y}.png`;
    geojsParams.layer.crossDomain = 'use-credentials';
    map.value = geo.map(geojsParams.map);
    map.value.clampBoundsX(false);
    map.value.createLayer('osm', geojsParams.layer);
  };

  watch(activeDataset, (newValue) => {
    if (!newValue?.id) {
      // Tear down the map if activeDataset goes to null
      map.value.exit();
    } else {
      updateBaseLayerDataset(newValue.id);
    }
  });

  return {
    map, center, zoom, zoomLevel, xCoord, yCoord, updateBaseLayerDataset,
  };
}
