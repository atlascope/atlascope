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

const inRangePinRadius = 10;
const maxPinRadius = 26;
const maxPinOpacity = 0.8;

function rampRadiusDown(currentZoom: number, minZoom: number) {
  return Math.max(0, inRangePinRadius - 5 * (minZoom - currentZoom));
}

function rampRadiusUp(maxZoom: number, currentZoom: number) {
  return Math.min(maxPinRadius, inRangePinRadius + 8 * (currentZoom - maxZoom));
}

export function radiusForZoomLevel(currentZoom: number, minZoom: number, maxZoom: number): number {
  if (currentZoom < minZoom) {
    return rampRadiusDown(currentZoom, minZoom);
  }
  if (currentZoom > maxZoom) {
    return rampRadiusUp(maxZoom, currentZoom);
  }
  return inRangePinRadius;
}

export function opacityForZoomLevel(currentZoom: number, maxZoom: number): number {
  if (currentZoom <= maxZoom) {
    return maxPinOpacity;
  }
  return Math.max(0, maxPinOpacity - 0.4 * (currentZoom - maxZoom));
}
