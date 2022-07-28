import { Dataset, DetectedStructure } from '@/generatedTypes/AtlascopeTypes';
import { computed } from '@vue/composition-api';
import geo from 'geojs';
import { GeoJSLayer } from './composableTypes';
import store from '../store';
import { centroidStringToCoords, NucleusGlandDistance } from './utiltyFunctions';

interface StructurePoint {
  x: number;
  y: number;
  color: string;
  struct: DetectedStructure;
}

const defaultStructureColors = {
  nucleus: 'green',
  gland: 'red',
};

function drawLines(target: StructurePoint) {
  const retArray: Array<Array<Array<number>>> = [];
  const computedLines = computed(() => store.state.nucleiToNearestGlandDistances);

  computedLines.value.forEach(
    (computedLine) => {
      if (
        computedLine[target.struct.structure_type as keyof NucleusGlandDistance]
         === target.struct.id
      ) {
        retArray.push(computedLine.line);
      }
    },
  );
  return retArray;
}

function visualizeDetectedStructures(
  data: Dataset,
  featureLayer: GeoJSLayer,
  color: string,
  structures: DetectedStructure[],
) {
  const structuresPoints = featureLayer.createFeature('point');
  const distanceLines = featureLayer.createFeature('line', {
    style: {
      strokeWidth: 1,
      strokeColor: 'yellow',
    },
  });
  const centroids = structures.map(
    (struct) => {
      const centroid = centroidStringToCoords(struct.centroid);
      return {
        x: centroid[0],
        y: centroid[1],
        color,
        struct,
      };
    },
  );
  structuresPoints.style({
    radius: 3,
    strokeColor: (point: StructurePoint) => point.color,
    fillColor: (point: StructurePoint) => point.color,
  });
  structuresPoints.addGeoEventHandler(geo.event.feature.mouseover, (event: typeof geo.event) => {
    const newData = centroids.map(
      (point) => {
        if (point === event.data) return Object.assign(event.data, { color: 'yellow' });
        return point;
      },
    );
    structuresPoints.data(newData);
    structuresPoints.draw();
    distanceLines.data(drawLines(event.data));
    distanceLines.draw();
  });
  structuresPoints.addGeoEventHandler(geo.event.feature.mouseout, () => {
    const newData = centroids.map(
      (point) => Object.assign(point, { color }),
    );
    structuresPoints.data(newData);
    structuresPoints.draw();
    distanceLines.data([]);
    distanceLines.draw();
  });
  structuresPoints.data(
    centroids,
  );
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
