import { Dataset, DetectedStructure } from '@/generatedTypes/AtlascopeTypes';
import { computed } from '@vue/composition-api';
import geo from 'geojs';
import { GeoJSLayer } from './composableTypes';
import store from '../store';
import { centroidStringToCoords, NucleusGlandDistance, Point } from './utiltyFunctions';

interface StructurePoint {
  x: number;
  y: number;
  color: string;
  structure: DetectedStructure;
}

const defaultStructureColors = {
  nucleus: 'green',
  gland: 'red',
};

function drawLines(target: StructurePoint) {
  const retArray: Point[][] = [];
  const computedLines = computed(() => store.state.nucleiToNearestGlandDistances);

  computedLines.value.forEach(
    (computedLine) => {
      if (
        computedLine[target.structure.structure_type as keyof NucleusGlandDistance]
         === target.structure.id
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
    (structure) => {
      const centroid = centroidStringToCoords(structure.centroid);
      return {
        x: centroid[0],
        y: centroid[1],
        color,
        structure,
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
          detectedStructures.value.filter((structure) => structure.detection_dataset === data.id),
        ),
      );
    } else {
      visualizeDetectedStructures(
        data, featureLayer, structureColor,
        detectedStructures.value.filter((structure) => structure.detection_dataset === data.id),
      );
    }
  }
}
