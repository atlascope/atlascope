import { DetectedStructure, VisOption } from '@/generatedTypes/AtlascopeTypes';
import { computed } from '@vue/composition-api';
import geo from 'geojs';
import { GeoJSLayer } from './composableTypes';
import store from '../store';
import { centroidStringToCoords, NucleusGlandDistance } from './utiltyFunctions';

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
  const retArray: Array<Array<Array<number>>> = [];
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

export function visualizeDetectedStructures(
  vis: VisOption,
  visLayer: GeoJSLayer,
  structures: DetectedStructure[],
) {
  const filteredStructures = structures.filter(
    (struct) => struct.detection_dataset === vis.data.id,
  );
  const structuresPoints = visLayer.createFeature('point');
  const color = defaultStructureColors[
    (vis.data.dataset_type?.replace('_detection', '') || 'nucleus') as keyof typeof defaultStructureColors
  ];
  const centroids = filteredStructures.map(
    (struct) => {
      const centroid = centroidStringToCoords(struct.centroid);
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
  if (vis.options.includes('show_distances_on_hover')) {
    const distanceLines = visLayer.createFeature('line', {
      style: {
        strokeWidth: 1,
        strokeColor: 'yellow',
      },
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
  }
  structuresPoints.data(
    centroids,
  );
  structuresPoints.draw();

  return true;
}

export default async function visualize(
  visList: VisOption[],
  visLayer: GeoJSLayer,
) {
  const detectedStructures = computed(() => store.state.detectedStuctures);
  if (detectedStructures.value.length < 1) {
    await store.dispatch.fetchDetectedStructures();
  }

  visList.forEach(
    (visOption) => {
      visOption.visFunc(visOption, visLayer, detectedStructures.value);
    },
  );
}
