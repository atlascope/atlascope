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
    // eslint-disable-next-line
    console.error(`Failed to convert location to point ${error}`);
  }
  return undefined;
}

export function getNonTiledImageDimensions(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject();
    image.src = url;
  });
}
