import { DetectedStructure } from '../generatedTypes/AtlascopeTypes';

export interface Point {
  x: number;
  y: number;
}

export function postGisToPoint(location: string): Point {
  const stringParts = location.split(' ');
  const xPart = stringParts[1];
  const yPart = stringParts[2];
  if (!xPart || !yPart) {
    throw new Error(`Unable to convert string ${location} to point.`);
  }
  const xCoord = parseInt(xPart.substring(1), 10);
  const yCoord = parseInt(yPart.substring(0, yPart.length - 1), 10);
  if (Number.isNaN(xCoord) || Number.isNaN(yCoord)) {
    throw new Error(`Unable to convert string ${location} to point.`);
  }
  return { x: xCoord, y: yCoord };
}

export function radiusForZoomLevel(currentZoom: number, minZoom: number, maxZoom: number): number {
  const inRangeRadius = 10;
  let diff = 0;
  if (currentZoom >= minZoom && currentZoom <= maxZoom) {
    return inRangeRadius;
  }
  if (currentZoom < minZoom) {
    diff = minZoom - currentZoom;
    if (diff > 2) {
      return 0;
    }
    return inRangeRadius - (5 * diff);
  }
  diff = currentZoom - maxZoom;
  if (diff > 2) {
    return inRangeRadius;
  }
  return inRangeRadius + (8 * diff);
}

export function opacityForZoomLevel(currentZoom: number, maxZoom: number): number {
  const maxOpacity = 0.8;
  if (currentZoom <= maxZoom) {
    return maxOpacity;
  }
  const diff = currentZoom - maxZoom;
  if (diff > 2) {
    return 0;
  }
  return maxOpacity - (0.4 * diff);
}

export function centroidStringToCoords(input: string): Array<number> {
  const centroidString = input.match(/\(([0-9|.|\s])+\)/);
  if (!centroidString) return [-1, -1];
  const centroid = centroidString[0].slice(1, -1).split(' ').map(
    (val: string) => parseFloat(val),
  );
  return centroid;
}

export interface NucleusGlandDistance{
  nucleus: number | undefined;
  gland: number | undefined;
  line: Array<Array<number>>;
}

export function nucleiToNearestGlandDistances(
  structures: DetectedStructure[],
): Array<NucleusGlandDistance> {
  const retArray: Array<NucleusGlandDistance> = [];
  const nuclei = structures.filter(
    (structure: DetectedStructure) => structure.structure_type === 'nucleus',
  );
  const glands = structures.filter(
    (structure: DetectedStructure) => structure.structure_type === 'gland',
  );

  nuclei.forEach(
    (nucleus) => {
      let minDistance: number;
      let nearestId: number | undefined;
      let minDistanceLine: Array<Array<number>> = [];
      const [x1, y1] = centroidStringToCoords(nucleus.centroid);
      glands.forEach(
        (gland) => {
          const [x2, y2] = centroidStringToCoords(gland.centroid);
          const distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
          if (!minDistance || distance < minDistance) {
            minDistance = distance;
            nearestId = gland.id;
            minDistanceLine = [[x1, y1], [x2, y2]];
          }
        },
      );
      retArray.push({
        nucleus: nucleus.id,
        gland: nearestId,
        line: minDistanceLine,
      });
    },
  );
  return retArray;
}
