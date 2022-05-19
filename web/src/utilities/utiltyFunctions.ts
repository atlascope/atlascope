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
