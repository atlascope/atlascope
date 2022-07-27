import { Dataset, DetectedStructure } from '@/generatedTypes/AtlascopeTypes';
import { computed } from '@vue/composition-api';
import { GeoJSLayer, GeoJSFeature } from './composableTypes';
import store from '../store';

const defaultStructureColors = {
  nucleus: 'green',
  gland: 'red',
};

// function transpose(array: Array<Array<number>>) {
//   return array[0].map(
//     (_: number, colIndex: number) => array.map((row: Array<number>) => row[colIndex]),
//   );
// }

// function flipXAxis(array: Array<Array<number>>) {
//   return array.map(
//     (subArray) => subArray.reverse(),
//   );
// }

function visualizeDetectedStructures(
  data: Dataset,
  featureLayer: GeoJSLayer,
  color: string,
  structures: DetectedStructure[],
) {
  // If we want to visualize the gland mask
  // in the future, we can get this grid working

  // if (!data?.metadata) return false;
  // let structureMask: Array<Array<number>> = [];
  // let numStructures;
  // Object.entries(data.metadata).forEach(
  //   ([key, value]) => {
  //     if (key.includes('num_')) numStructures = value;
  //     if (key.includes('_mask')) structureMask = value;
  //   },
  // );
  // const grid: GeoJSFeature = featureLayer.createFeature('grid', {
  //   grid: {
  //     gridWidth: structureMask[0].length,
  //     gridHeight: structureMask.length,
  //     x0: 0,
  //     y0: 0,
  //     dx: 1,
  //     dy: 1,
  //   },
  // });
  // console.log(numStructures, 'detected.');
  // grid.data(structureMask.flat());
  // // .map(
  // //   (value) => (value === 0 ? undefined : value),
  // // ));
  // grid.draw();

  const structuresPoints = featureLayer.createFeature('point');
  const centroids = structures.map(
    (struct) => {
      const centroidString = struct.centroid.match(/\(([0-9|.|\s])+\)/);
      if (!centroidString) return { x: undefined, y: undefined };
      const centroid = centroidString[0].slice(1, -1).split(' ');
      return {
        x: centroid[0],
        y: centroid[1],
      };
    },
  );
  structuresPoints.data(
    centroids,
  );
  // structuresPoints.position((pin: Pin) => postGisToPoint(pin.location));
  structuresPoints.style({
    radius: 2,
    strokeColor: color,
    fillColor: color,
  });
  structuresPoints.draw();
  return true;
}

export default function visualize(
  data: Dataset,
  featureLayer: GeoJSLayer | undefined,
) {
  if (!featureLayer) {
    return;
  }
  if (data.dataset_type === 'nucleus_detection' || data.dataset_type === 'gland_detection') {
    const detectedStructures = computed(() => store.state.detectedStuctures);
    const structureColor: string = defaultStructureColors[
      data.dataset_type.replace('_detection', '') as keyof typeof defaultStructureColors
    ];
    if (detectedStructures.value.length < 1) {
      store.dispatch.fetchDetectedStructures().then(
        () => visualizeDetectedStructures(
          data, featureLayer, structureColor,
          detectedStructures.value.filter((struct) => struct.detection_dataset === data.id),
        ),
      );
    } else {
      visualizeDetectedStructures(
        data, featureLayer, structureColor,
        detectedStructures.value.filter((struct) => struct.detection_dataset === data.id),
      );
    }
  }
}
