export type InvestigationID = number;
export type DatasetID = string;
export type DatasetEmbeddingID = string;

export interface DatasetEmbedding {
  id: DatasetEmbeddingID;
  child_bounding_box: [number, number, number, number];
  parent: DatasetID;
  child: DatasetID;
  [key:string]: any;
}

export interface TileMetadata {
  levels: number;
  size_x: number;
  size_y: number;
  tile_size: number;
}

// demo only type - embedded info in `DatasetID`
export interface DatasetInfo {
  color: string;
  size_x: number;
  size_y: number;
  depth: number;
}
const datasetIDregex = /(?<color>\w+)-(?<size_x>\d+)-(?<size_y>\d+)-(?<depth>\d+)/;
const makeDatasetID = (info: DatasetInfo): DatasetID => `${info.color}-${info.size_x}-${info.size_y}-${info.depth}`;
// @ts-ignore
const makeDatasetInfo = (id: DatasetID): DatasetInfo => datasetIDregex.exec(id).groups;

const TILE_SIZE = 256;

// https://stackoverflow.com/a/65793426
class SeedRand {
  seed: number;
  constructor(seed: number) {
    this.seed = seed;
  }
  rand(): number {
    this.seed = ((this.seed + 0x7ED55D16) + (this.seed << 12))  & 0xFFFFFFFF;
    this.seed = ((this.seed ^ 0xC761C23C) ^ (this.seed >>> 19)) & 0xFFFFFFFF;
    this.seed = ((this.seed + 0x165667B1) + (this.seed << 5))   & 0xFFFFFFFF;
    this.seed = ((this.seed + 0xD3A2646C) ^ (this.seed << 9))   & 0xFFFFFFFF;
    this.seed = ((this.seed + 0xFD7046C5) + (this.seed << 3))   & 0xFFFFFFFF;
    this.seed = ((this.seed ^ 0xB55A4F09) ^ (this.seed >>> 16)) & 0xFFFFFFFF;
    return (this.seed & 0xFFFFFFF) / 0x10000000;
  }
  randInt(floor: number, ceil: number): number {
    return floor + Math.floor(this.rand() * (1 + ceil - floor));
  }
  randElement<Type>(a: Array<Type>): Type  {
    return a[this.randInt(0, a.length - 1)];
  }
}

export function getEmbeddings(investigationID: InvestigationID): Array<DatasetEmbedding> {
  const rand = new SeedRand(investigationID);
  const embeddings: Array<DatasetEmbedding> = [];
  const colors: Array<string> = ["red", "green", "blue", "yellow"];
  const datasetInfoFactory = (color: string): DatasetInfo => {
    const width = 2 ** rand.randInt(3, 8) * TILE_SIZE;
    return {
      color,
      size_x: width,
      size_y: rand.randInt(Math.ceil(1.05*width), Math.ceil(1.2*width)),
      depth: embeddings.length,
    }
  };
  const embeddingFactory = (parentInfo: DatasetInfo): DatasetEmbedding => {
    const width = rand.randInt(Math.ceil(0.05*parentInfo.size_x), Math.ceil(0.2*parentInfo.size_x));
    const height = rand.randInt(Math.ceil(1.05*width), Math.ceil(1.2*width));
    const x0 = rand.randInt(0, parentInfo.size_x - width);
    const y0 = rand.randInt(0, parentInfo.size_y - height);
    return {
      id: `${embeddings.length}`,
      child_bounding_box: [x0+width, y0+height, x0, y0],
      parent: makeDatasetID(parentInfo),
      child: makeDatasetID(datasetInfoFactory(rand.randElement(colors.filter(c => c !== parentInfo.color)))),
    };
  };
  // Root node
  let parentInfo = datasetInfoFactory(rand.randElement(colors));
  embeddings.push(embeddingFactory(parentInfo));
  // Add children
  while (rand.randInt(0, 1)) {
    let randomEmbedding = rand.randElement(embeddings);
    let randomDatasetID = rand.randInt(0, 1) ? randomEmbedding.parent : randomEmbedding.child;
    let parentInfo = makeDatasetInfo(randomDatasetID);
    embeddings.push(embeddingFactory(parentInfo));
  };
  return embeddings;
};

export function getTileMetadata(datasetID: DatasetID): TileMetadata {
  const datasetInfo = makeDatasetInfo(datasetID);
  return {
    levels: Math.floor(Math.log2(Math.max(datasetInfo.size_x, datasetInfo.size_y) / TILE_SIZE)),
    size_x: datasetInfo.size_x,
    size_y: datasetInfo.size_y,
    tile_size: TILE_SIZE,
  };
}
