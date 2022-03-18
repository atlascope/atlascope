<template>
  <v-container
    class="grey lighten-3 pa-0 ma-0"
    fill-height
  >
    <div
      id="map"
      ref="mapElement"
    />
  </v-container>
</template>

<style scoped>
#map {
  width: 500px;
  height: 500px;
  padding: 0;
  margin: 0;
}
</style>

<script lang="ts">
import {
  ref, defineComponent, onMounted, PropType, computed,
} from '@vue/composition-api';
import geo from 'geojs';
import { getEmbeddings, getTileMetadata } from '../datasets';
import type { DatasetEmbedding, DatasetID } from '../datasets';

interface RootDatasetEmbedding {
  id: null;
  child_bounding_box: [number, number, number, number];
  parent: null;
  child: DatasetID;
  [key: string]: any;
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

  setup() {
    const mapElement = ref(null);

    onMounted(async () => {
      const embeddings: Array<DatasetEmbedding> = getEmbeddings(2);
      const rootDatasetID: DatasetID = embeddings.find((e) => embeddings.every((x) => x.child !== e.parent)).parent;
      const rootTileMetadata = getTileMetadata(rootDatasetID);
      const rootMinLevel = Math.min(
        0,
        Math.floor(
          Math.log2(Math.min(500 / rootTileMetadata.tile_size, 500 / rootTileMetadata.tile_size)),
        ),
      );
      const rootMaxLevel = Math.ceil(
        Math.log2(
          Math.max(
            rootTileMetadata.size_x / rootTileMetadata.tile_size,
            rootTileMetadata.size_y / rootTileMetadata.tile_size,
          ),
        ),
      );

      console.log('datasetID', rootDatasetID);
      console.log('treeDepth', 0);
      console.log('tileMetadata', rootTileMetadata);
      console.log('embedding', null);
      console.log('minLevel', rootMinLevel);
      console.log('maxLevel', rootMaxLevel);
      console.log('scale', 1);
      console.log('offset', { x: 0, y: 0 });

      const map = geo.map({
        node: mapElement.value,
        ingcs: '+proj=longlat +axis=esu',
        gcs: '+proj=longlat +axis=enu',
        maxBounds: {
          left: 0,
          top: 0,
          right: rootTileMetadata.size_x,
          bottom: rootTileMetadata.size_y,
        },
        unitsPerPixel: 2 ** rootMaxLevel,
        center: {
          x: rootTileMetadata.size_x / 2,
          y: rootTileMetadata.size_y / 2,
        },
        min: rootMinLevel,
        max: rootMaxLevel + 10,
        zoom: rootMinLevel,
        clampBoundsX: true,
        clampBoundsY: true,
        clampZoom: true,
      });

      map.createLayer('osm', {
        url: (x: number, y: number, z: number) => `http://localhost:9005/${rootDatasetID}/${z}/${y}/${x}.png`,
        zIndex: 0,
        minLevel: rootMinLevel,
        maxLevel: rootMaxLevel,
        wrapX: false,
        wrapY: false,
        tileOffset(level: number) {
          return { x: 0, y: 0 };
        },
        attribution: '',
        tileWidth: rootTileMetadata.tile_size,
        tileHeight: rootTileMetadata.tile_size,
        tileRounding: Math.ceil,
        tilesAtZoom(level: number) {
          return {
            x: Math.ceil(
              rootTileMetadata.size_x / rootTileMetadata.tile_size / 2 ** (rootMaxLevel - level),
            ),
            y: Math.ceil(
              rootTileMetadata.size_y / rootTileMetadata.tile_size / 2 ** (rootMaxLevel - level),
            ),
          };
        },
        tilesMaxBounds(level: number) {
          return {
            x: Math.floor(rootTileMetadata.size_x / 2 ** (rootMaxLevel - level)),
            y: Math.floor(rootTileMetadata.size_y / 2 ** (rootMaxLevel - level)),
          };
        },
      });

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
        const tileMetadata = getTileMetadata(datasetID);

        const scale = Math.min(
          (parent.scale * (embedding.child_bounding_box[0] - embedding.child_bounding_box[2]))
            / tileMetadata.size_x,
          (parent.scale * (embedding.child_bounding_box[1] - embedding.child_bounding_box[3]))
            / tileMetadata.size_y,
        );
        const offset = {
          x: (parent.scale / scale) * (parent.offset.x + embedding.child_bounding_box[2]),
          y: (parent.scale / scale) * (parent.offset.y + embedding.child_bounding_box[3]),
        };

        const minLevel = Math.min(
          Math.log2(rootTileMetadata.size_x / (scale * tileMetadata.size_x)),
          Math.log2(rootTileMetadata.size_y / (scale * tileMetadata.size_y)),
        );
        const maxLevel = tileMetadata.levels
          + Math.min(
            Math.log2(rootTileMetadata.size_x / (scale * tileMetadata.size_x)),
            Math.log2(rootTileMetadata.size_y / (scale * tileMetadata.size_y)),
          );

        console.log('datasetID', datasetID);
        console.log('treeDepth', treeDepth);
        console.log('tileMetadata', tileMetadata);
        console.log('embedding', embedding);
        console.log('minLevel', minLevel);
        console.log('maxLevel', maxLevel);
        console.log('scale', scale);
        console.log('offset', offset);

        const layer = map.createLayer('osm', {
          url: (x: number, y: number, z: number) => `http://localhost:9005/${datasetID}/${z}/${y}/${x}.png`,
          zIndex: treeDepth,
          minLevel: 0,
          maxLevel: Math.ceil(rootMaxLevel),
          wrapX: false,
          wrapY: false,
          tileOffset(level: number) {
            return {
              x: 0,
              y: 0,
            };
          },
          attribution: '',
          tileWidth: tileMetadata.tile_size,
          tileHeight: tileMetadata.tile_size,
          tileRounding: Math.ceil,
          tilesAtZoom(level: number) {
            return {
              x: Math.ceil(
                tileMetadata.size_x / tileMetadata.tile_size / 2 ** (rootMaxLevel - level),
              ),
              y: Math.ceil(
                tileMetadata.size_y / tileMetadata.tile_size / 2 ** (rootMaxLevel - level),
              ),
            };
          },
          tilesMaxBounds(level: number) {
            return {
              x: Math.floor(tileMetadata.size_x / 2 ** (rootMaxLevel - level)),
              y: Math.floor(tileMetadata.size_y / 2 ** (rootMaxLevel - level)),
            };
          },
        });
        layer.gcs(
          `+proj=longlat +axis=enu +xoff=-${offset.x} +yoff=${offset.y} +s11=${1 / scale} +s22=${
            1 / scale
          }`,
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
    return { mapElement };
  },
});
</script>
