<template>
  <v-container
    class="grey lighten-3 pa-0 ma-0"
    fill-height
  >
    <div
      ref="map"
      class="map"
    />
  </v-container>
</template>

<style scoped>
.map {
  width: 500px;
  height: 500px;
  padding: 0;
  margin: 0;
}
</style>

<script lang="ts">
import {
  ref, defineComponent, onMounted, PropType, Ref,
} from '@vue/composition-api';
import type { DatasetEmbedding } from '../generatedTypes/AtlascopeTypes';
import store from '../store';
import useGeoJS from '../utilities/useGeoJS';

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
  name: 'EmbeddingsDetail',

  props: {
    investigation: {
      type: String as PropType<string>,
      required: true,
    },
  },

  setup(props) {
    const map: Ref<null | HTMLElement> = ref(null);
    const {
      generatePixelCoordinateParams,
      createMap,
      createLayer,
    } = useGeoJS(map);

    onMounted(async () => {
      await store.dispatch.fetchCurrentInvestigation(props.investigation);
      const apiRoot = process.env.VUE_APP_API_ROOT;
      const embeddings = store.state.datasetEmbeddings;
      const rootDatasetID = embeddings.find(
        (e) => embeddings.every(
          (x) => x.child !== e.parent,
        ),
      ).parent;
      const rootTileMetadata = store.state.datasetTileMetadata[rootDatasetID];
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
      createLayer('osm', rootLayerParams);

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
        const datasetID = embedding.child;
        const tileMetadata = store.state.datasetTileMetadata[datasetID];
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
          (parent.scale * (boundingBox.x.max - boundingBox.x.min)) / tileMetadata.size_x,
          (parent.scale * (boundingBox.y.max - boundingBox.y.min)) / tileMetadata.size_y,
        );
        const offset = {
          x: (parent.scale / scale) * (parent.offset.x + boundingBox.x.min),
          y: (parent.scale / scale) * (parent.offset.y + boundingBox.y.min),
        };
        const minLevel = Math.min(
          Math.log2(rootTileMetadata.size_x / (scale * tileMetadata.size_x)),
          Math.log2(rootTileMetadata.size_y / (scale * tileMetadata.size_y)),
        );
        const maxLevel = tileMetadata.levels + Math.min(
          Math.log2(rootTileMetadata.size_x / (scale * tileMetadata.size_x)),
          Math.log2(rootTileMetadata.size_y / (scale * tileMetadata.size_y)),
        );
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
          `+proj=longlat +axis=enu +xoff=-${offset.x} +yoff=${offset.y} +s11=${1 / scale} +s22=${1 / scale}`,
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
    });

    return { map };
  },
});
</script>
