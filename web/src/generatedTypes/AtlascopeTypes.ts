/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface Dataset {
  /** ID */
  id?: number;

  /** Name */
  name: string;

  /** Description */
  description?: string;

  /**
   * Content
   * @format uri
   */
  content?: string | null;

  /** Metadata */
  metadata?: object | null;

  /** Dataset type */
  dataset_type?: "tile_source" | "tile_overlay" | "analytics" | "subimage" | "non_tiled_image";

  /** Source dataset */
  source_dataset?: number | null;
  derived_datasets: number[];
  child_embeddings: number[];
  parent_embeddings: number[];
  jobs: number[];
  origin: number[];
  pins: number[];
  locations: number[];
}

export interface DatasetCreate {
  /** Name */
  name?: string;

  /** Description */
  description?: string;

  /** Dataset type */
  dataset_type?: "tile_source" | "tile_overlay" | "analytics" | "subimage" | "non_tiled_image";

  /**
   * Importer
   * The importer module to invoke.            Must be one of ['UploadImporter', 'VandyImporter'].
   */
  importer?: string;

  /**
   * Import arguments
   * Any arguments to supply to the selected importer function
   */
  import_arguments: object;
}

export interface DatasetSubImage {
  /** X0 */
  x0: number;

  /** Y0 */
  y0: number;

  /** X1 */
  x1: number;

  /** Y1 */
  y1: number;
}

export interface Investigation {
  /** ID */
  id?: number;

  /** Name */
  name: string;

  /** Description */
  description?: string;
  datasets: number[];
  pins: number[];

  /** Notes */
  notes?: string;

  /**
   * Created
   * @format date-time
   */
  created?: string;

  /**
   * Modified
   * @format date-time
   */
  modified?: string;
  embeddings: number[];
  jobs: number[];
}

export interface DatasetEmbedding {
  /** ID */
  id?: number;
  child_bounding_box?: number[];

  /** Investigation */
  investigation: number;

  /** Parent */
  parent: number;

  /** Child */
  child: number;
}

export interface JobDetail {
  /** ID */
  id?: number;

  /** Complete */
  complete?: boolean;

  /** Job type */
  job_type?: string;

  /** Additional inputs */
  additional_inputs?: object | null;

  /** Investigation */
  investigation: number;

  /** Original dataset */
  original_dataset: number;
  resulting_datasets: number[];
}

export interface Pin {
  /** ID */
  id?: number;

  /** Child location */
  child_location: string;

  /** Color */
  color?: "red" | "blue" | "green" | "orange" | "purple" | "black";

  /** Note */
  note?: string;

  /**
   * Minimum zoom
   * @min 0
   * @max 2147483647
   */
  minimum_zoom?: number;

  /**
   * Maximum zoom
   * @min 0
   * @max 2147483647
   */
  maximum_zoom?: number;

  /** Investigation */
  investigation: number;

  /** Parent */
  parent: number;

  /** Child */
  child?: number | null;
}

export interface JobSpawn {
  /** Investigation */
  investigation: number;

  /** Job type */
  job_type?: string;

  /** Original dataset */
  original_dataset: number;

  /** Additional inputs */
  additional_inputs?: object | null;
}

export interface DatasetsListParams {
  /** Number of results to return per page. */
  limit?: number;

  /** The initial index from which to return the results. */
  offset?: number;
}

export interface DatasetsTileSourceBandParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** The band number to use. */
  band?: number;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceBandsParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceHistogramParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;
  onlyMinMax?: boolean;
  bins?: number;
  density?: boolean;
  format?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceMetadataParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceMetadataInternalParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourcePixelParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** left */
  left: number;

  /** top */
  top: number;

  /** The color palette to map the band values (named Matplotlib colormaps or palettable palettes). `cmap` alias supported. */
  palette?: string;

  /** The band number to use. */
  band?: number;

  /** The minimum value for the color mapping. */
  min?: number;

  /** The maximum value for the color mapping. */
  max?: number;

  /** The value to map as no data (often made transparent). */
  nodata?: number;

  /** This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values). */
  scheme?: string;

  /** Encoded string of JSON style following https://girder.github.io/large_image/tilesource_options.html#style */
  style?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceRegionJpegParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** left */
  left: number;

  /** right */
  right: number;

  /** top */
  top: number;

  /** bottom */
  bottom: number;

  /** The projection/units of the region coordinates. */
  units?: string;

  /** The color palette to map the band values (named Matplotlib colormaps or palettable palettes). `cmap` alias supported. */
  palette?: string;

  /** The band number to use. */
  band?: number;

  /** The minimum value for the color mapping. */
  min?: number;

  /** The maximum value for the color mapping. */
  max?: number;

  /** The value to map as no data (often made transparent). */
  nodata?: number;

  /** This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values). */
  scheme?: string;

  /** Encoded string of JSON style following https://girder.github.io/large_image/tilesource_options.html#style */
  style?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceRegionPngParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** left */
  left: number;

  /** right */
  right: number;

  /** top */
  top: number;

  /** bottom */
  bottom: number;

  /** The projection/units of the region coordinates. */
  units?: string;

  /** The color palette to map the band values (named Matplotlib colormaps or palettable palettes). `cmap` alias supported. */
  palette?: string;

  /** The band number to use. */
  band?: number;

  /** The minimum value for the color mapping. */
  min?: number;

  /** The maximum value for the color mapping. */
  max?: number;

  /** The value to map as no data (often made transparent). */
  nodata?: number;

  /** This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values). */
  scheme?: string;

  /** Encoded string of JSON style following https://girder.github.io/large_image/tilesource_options.html#style */
  style?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceRegionTifParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** left */
  left: number;

  /** right */
  right: number;

  /** top */
  top: number;

  /** bottom */
  bottom: number;

  /** The projection/units of the region coordinates. */
  units?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceThumbnailJpegParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** maximum height in pixels. */
  max_height?: number;

  /** maximum width in pixels. */
  max_width?: number;

  /** The color palette to map the band values (named Matplotlib colormaps or palettable palettes). `cmap` alias supported. */
  palette?: string;

  /** The band number to use. */
  band?: number;

  /** The minimum value for the color mapping. */
  min?: number;

  /** The maximum value for the color mapping. */
  max?: number;

  /** The value to map as no data (often made transparent). */
  nodata?: number;

  /** This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values). */
  scheme?: string;

  /** Encoded string of JSON style following https://girder.github.io/large_image/tilesource_options.html#style */
  style?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceThumbnailPngReadParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** maximum height in pixels. */
  max_height?: number;

  /** maximum width in pixels. */
  max_width?: number;

  /** The color palette to map the band values (named Matplotlib colormaps or palettable palettes). `cmap` alias supported. */
  palette?: string;

  /** The band number to use. */
  band?: number;

  /** The minimum value for the color mapping. */
  min?: number;

  /** The maximum value for the color mapping. */
  max?: number;

  /** The value to map as no data (often made transparent). */
  nodata?: number;

  /** This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values). */
  scheme?: string;

  /** Encoded string of JSON style following https://girder.github.io/large_image/tilesource_options.html#style */
  style?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceTilesMetadataReadParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceTileJpegParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** The color palette to map the band values (named Matplotlib colormaps or palettable palettes). `cmap` alias supported. */
  palette?: string;

  /** The band number to use. */
  band?: number;

  /** The minimum value for the color mapping. */
  min?: number;

  /** The maximum value for the color mapping. */
  max?: number;

  /** The value to map as no data (often made transparent). */
  nodata?: number;

  /** This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values). */
  scheme?: string;

  /** Encoded string of JSON style following https://girder.github.io/large_image/tilesource_options.html#style */
  style?: string;

  /** A unique integer value identifying this dataset. */
  id: number;

  /** The 0-based X position of the tile on the specified Z level. */
  x: number;

  /** The 0-based Y position of the tile on the specified Z level. */
  y: number;

  /** The Z level of the tile. May range from [0, levels], where 0 is the lowest resolution, single tile for the whole source. */
  z: number;
}

export interface DatasetsTileSourceTilePngParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** The color palette to map the band values (named Matplotlib colormaps or palettable palettes). `cmap` alias supported. */
  palette?: string;

  /** The band number to use. */
  band?: number;

  /** The minimum value for the color mapping. */
  min?: number;

  /** The maximum value for the color mapping. */
  max?: number;

  /** The value to map as no data (often made transparent). */
  nodata?: number;

  /** This is either ``linear`` (the default) or ``discrete``. If a palette is specified, ``linear`` uses a piecewise linear interpolation, and ``discrete`` uses exact colors from the palette with the range of the data mapped into the specified number of colors (e.g., a palette with two colors will split exactly halfway between the min and max values). */
  scheme?: string;

  /** Encoded string of JSON style following https://girder.github.io/large_image/tilesource_options.html#style */
  style?: string;

  /** A unique integer value identifying this dataset. */
  id: number;

  /** The 0-based X position of the tile on the specified Z level. */
  x: number;

  /** The 0-based Y position of the tile on the specified Z level. */
  y: number;

  /** The Z level of the tile. May range from [0, levels], where 0 is the lowest resolution, single tile for the whole source. */
  z: number;
}

export interface DatasetsTileSourceTilesTileCornersParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;

  /** The 0-based X position of the tile on the specified Z level. */
  x: number;

  /** The 0-based Y position of the tile on the specified Z level. */
  y: number;

  /** The Z level of the tile. May range from [0, levels], where 0 is the lowest resolution, single tile for the whole source. */
  z: number;
}

export interface InvestigationsListParams {
  /** Number of results to return per page. */
  limit?: number;

  /** The initial index from which to return the results. */
  offset?: number;
}

export interface JobsListParams {
  /** Number of results to return per page. */
  limit?: number;

  /** The initial index from which to return the results. */
  offset?: number;
}

export interface JobsTypesParams {
  /** Number of results to return per page. */
  limit?: number;

  /** The initial index from which to return the results. */
  offset?: number;
}

export namespace Datasets {
  /**
   * No description
   * @tags datasets
   * @name DatasetsList
   * @request GET:/datasets
   * @response `200` `{ count: number, next?: string | null, previous?: string | null, results: (Dataset)[] }`
   */
  export namespace DatasetsList {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = { count: number; next?: string | null; previous?: string | null; results: Dataset[] };
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsCreate
   * @request POST:/datasets
   * @response `201` `DatasetCreate`
   */
  export namespace DatasetsCreate {
    export type RequestParams = {};
    export type RequestQuery = {};
    export type RequestBody = DatasetCreate;
    export type RequestHeaders = {};
    export type ResponseBody = DatasetCreate;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceBand
   * @summary Returns bands information.
   * @request GET:/datasets/tile_source/{id}/band
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceBand {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string; band?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceBands
   * @summary Returns bands information.
   * @request GET:/datasets/tile_source/{id}/bands
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceBands {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceHistogram
   * @summary Returns histogram
   * @request GET:/datasets/tile_source/{id}/histogram
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceHistogram {
    export type RequestParams = { id: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      onlyMinMax?: boolean;
      bins?: number;
      density?: boolean;
      format?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceMetadata
   * @summary Returns tile metadata.
   * @request GET:/datasets/tile_source/{id}/metadata
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceMetadata {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceMetadataInternal
   * @summary Returns additional known metadata about the tile source.
   * @request GET:/datasets/tile_source/{id}/metadata_internal
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceMetadataInternal {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourcePixel
   * @summary Returns single pixel.
   * @request GET:/datasets/tile_source/{id}/pixel
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourcePixel {
    export type RequestParams = { id: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      left: number;
      top: number;
      palette?: string;
      band?: number;
      min?: number;
      max?: number;
      nodata?: number;
      scheme?: string;
      style?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceRegionJpeg
   * @summary Returns region tile binary.
   * @request GET:/datasets/tile_source/{id}/region.jpeg
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceRegionJpeg {
    export type RequestParams = { id: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      left: number;
      right: number;
      top: number;
      bottom: number;
      units?: string;
      palette?: string;
      band?: number;
      min?: number;
      max?: number;
      nodata?: number;
      scheme?: string;
      style?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceRegionPng
   * @summary Returns region tile binary.
   * @request GET:/datasets/tile_source/{id}/region.png
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceRegionPng {
    export type RequestParams = { id: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      left: number;
      right: number;
      top: number;
      bottom: number;
      units?: string;
      palette?: string;
      band?: number;
      min?: number;
      max?: number;
      nodata?: number;
      scheme?: string;
      style?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceRegionTif
   * @summary Returns region tile binary.
   * @request GET:/datasets/tile_source/{id}/region.tif
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceRegionTif {
    export type RequestParams = { id: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      left: number;
      right: number;
      top: number;
      bottom: number;
      units?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceThumbnailJpeg
   * @summary Returns thumbnail of full image.
   * @request GET:/datasets/tile_source/{id}/thumbnail.jpeg
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceThumbnailJpeg {
    export type RequestParams = { id: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      max_height?: number;
      max_width?: number;
      palette?: string;
      band?: number;
      min?: number;
      max?: number;
      nodata?: number;
      scheme?: string;
      style?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceThumbnailPngRead
   * @summary Returns thumbnail of full image.
   * @request GET:/datasets/tile_source/{id}/thumbnail.png
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceThumbnailPngRead {
    export type RequestParams = { id: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      max_height?: number;
      max_width?: number;
      palette?: string;
      band?: number;
      min?: number;
      max?: number;
      nodata?: number;
      scheme?: string;
      style?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceTiffdump
   * @summary Returns tifftools tiffdump JSON. This will raise a `ValidationError` if the image is not a Tiff.
   * @request GET:/datasets/tile_source/{id}/tiffdump
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceTiffdump {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceTilesMetadataRead
   * @summary Returns tile metadata.
   * @request GET:/datasets/tile_source/{id}/tiles/metadata
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceTilesMetadataRead {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceTileJpeg
   * @summary Returns tile image binary.
   * @request GET:/datasets/tile_source/{id}/tiles/{z}/{x}/{y}.jpeg
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceTileJpeg {
    export type RequestParams = { id: number; x: number; y: number; z: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      palette?: string;
      band?: number;
      min?: number;
      max?: number;
      nodata?: number;
      scheme?: string;
      style?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceTilePng
   * @summary Returns tile image binary.
   * @request GET:/datasets/tile_source/{id}/tiles/{z}/{x}/{y}.png
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceTilePng {
    export type RequestParams = { id: number; x: number; y: number; z: number };
    export type RequestQuery = {
      projection?: string;
      source?: string;
      palette?: string;
      band?: number;
      min?: number;
      max?: number;
      nodata?: number;
      scheme?: string;
      style?: string;
    };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceTilesTileCorners
   * @summary Returns bounds of a tile for a given x, y, z index.
   * @request GET:/datasets/tile_source/{id}/tiles/{z}/{x}/{y}/corners
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceTilesTileCorners {
    export type RequestParams = { id: number; x: number; y: number; z: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsRead
   * @request GET:/datasets/{id}
   * @response `200` `Dataset`
   */
  export namespace DatasetsRead {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsSubimage
   * @request POST:/datasets/{id}/subimage
   * @response `201` `DatasetSubImage`
   */
  export namespace DatasetsSubimage {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = DatasetSubImage;
    export type RequestHeaders = {};
    export type ResponseBody = DatasetSubImage;
  }
}

export namespace Investigations {
  /**
   * No description
   * @tags investigations
   * @name InvestigationsList
   * @request GET:/investigations
   * @response `200` `{ count: number, next?: string | null, previous?: string | null, results: (Investigation)[] }`
   */
  export namespace InvestigationsList {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = {
      count: number;
      next?: string | null;
      previous?: string | null;
      results: Investigation[];
    };
  }
  /**
   * No description
   * @tags investigations
   * @name InvestigationsRead
   * @request GET:/investigations/{id}
   * @response `200` `Investigation`
   */
  export namespace InvestigationsRead {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Investigation;
  }
  /**
   * No description
   * @tags investigations
   * @name InvestigationsEmbeddings
   * @request GET:/investigations/{id}/embeddings
   * @response `200` `(DatasetEmbedding)[]`
   */
  export namespace InvestigationsEmbeddings {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = DatasetEmbedding[];
  }
  /**
   * No description
   * @tags investigations
   * @name InvestigationsJobs
   * @request GET:/investigations/{id}/jobs
   * @response `200` `(JobDetail)[]`
   */
  export namespace InvestigationsJobs {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = JobDetail[];
  }
  /**
   * No description
   * @tags investigations
   * @name InvestigationsPins
   * @request GET:/investigations/{id}/pins
   * @response `200` `(Pin)[]`
   */
  export namespace InvestigationsPins {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Pin[];
  }
}

export namespace Jobs {
  /**
   * No description
   * @tags jobs
   * @name JobsList
   * @request GET:/jobs
   * @response `200` `{ count: number, next?: string | null, previous?: string | null, results: (JobDetail)[] }`
   */
  export namespace JobsList {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = { count: number; next?: string | null; previous?: string | null; results: JobDetail[] };
  }
  /**
   * No description
   * @tags jobs
   * @name JobsCreate
   * @request POST:/jobs
   * @response `201` `JobSpawn`
   */
  export namespace JobsCreate {
    export type RequestParams = {};
    export type RequestQuery = {};
    export type RequestBody = JobSpawn;
    export type RequestHeaders = {};
    export type ResponseBody = JobSpawn;
  }
  /**
   * @description Retrieve a list of available options for job_type on Jobs
   * @tags jobs
   * @name JobsTypes
   * @request GET:/jobs/types
   * @response `200` `object`
   */
  export namespace JobsTypes {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = object;
  }
  /**
   * No description
   * @tags jobs
   * @name JobsRead
   * @request GET:/jobs/{id}
   * @response `200` `JobDetail`
   */
  export namespace JobsRead {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = JobDetail;
  }
  /**
   * No description
   * @tags jobs
   * @name JobsRerun
   * @request POST:/jobs/{id}/rerun
   * @response `204` `void` Rerun spawned.
   */
  export namespace JobsRerun {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = void;
  }
}
