export interface Point {
  x: number;
  y: number;
}

export function postGisToPoint(location: string): Point | undefined {
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

export function radiusForZoomLevel(currentZoom: number, minZoom: number): number {
  const maxRadius = 10;
  if (currentZoom >= minZoom) {
    return maxRadius;
  }
  const diff = minZoom - currentZoom;
  if (diff > 2) {
    return 0;
  }
  return maxRadius - (5 * diff);
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
