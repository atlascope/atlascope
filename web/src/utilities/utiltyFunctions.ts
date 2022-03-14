export interface Point {
  x: number;
  y: number;
}

export function postGisToPoint(location: string): Point | undefined {
  try {
    const stringParts = location.split(' ');
    const xPart = stringParts[1];
    const yPart = stringParts[2];
    return {
      x: parseInt(xPart.substring(1), 10),
      y: parseInt(yPart.substring(0, yPart.length - 1), 10),
    };
  } catch (error) {
    console.error(`Failed to convert location to point ${error}`);
  }
  return undefined;
}