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
  dataset_type?: string;

  /** Source dataset */
  source_dataset?: number | null;
  derived_datasets: number[];
  child_embeddings: number[];
  parent_embeddings: number[];
  jobs: number[];
  origin: number[];
  pins: number[];
  locations: string[];
  detected_structures: number[];
}

export interface DatasetCreate {
  /** Name */
  name?: string;

  /** Description */
  description?: string;

  /** Dataset type */
  dataset_type?: string;

  /**
   * Importer
   * The importer module to invoke.            Must be one of ['UploadImporter', 'VandyImporter', 'GoogleDriveImporter'].
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

  /** Investigation */
  investigation: string;
}

export interface DetectedStructure {
  /** ID */
  id?: number;

  /**
   * Label integer
   * @min -2147483648
   * @max 2147483647
   */
  label_integer: number;

  /** Centroid */
  centroid: string;

  /** Weighted centroid */
  weighted_centroid: string;

  /** Bounding box */
  bounding_box: string;

  /** Gradient canny mean */
  gradient_canny_mean: number;

  /** Gradient canny sum */
  gradient_canny_sum: number;

  /** Gradient mag histenergy */
  gradient_mag_histenergy: number;

  /** Gradient mag histentropy */
  gradient_mag_histentropy: number;

  /** Gradient mag kurtosis */
  gradient_mag_kurtosis: number;

  /** Gradient mag mean */
  gradient_mag_mean: number;

  /** Gradient mag skewness */
  gradient_mag_skewness: number;

  /** Gradient mag std */
  gradient_mag_std: number;

  /** Haralick asm mean */
  haralick_asm_mean: number;

  /** Haralick asm range */
  haralick_asm_range: number;

  /** Haralick contrast mean */
  haralick_contrast_mean: number;

  /** Haralick contrast range */
  haralick_contrast_range: number;

  /** Haralick correlation mean */
  haralick_correlation_mean: number;

  /** Haralick correlation range */
  haralick_correlation_range: number;

  /** Haralick differenceentropy mean */
  haralick_differenceentropy_mean: number;

  /** Haralick differenceentropy range */
  haralick_differenceentropy_range: number;

  /** Haralick differencevariance mean */
  haralick_differencevariance_mean: number;

  /** Haralick differencevariance range */
  haralick_differencevariance_range: number;

  /** Haralick entropy mean */
  haralick_entropy_mean: number;

  /** Haralick entropy range */
  haralick_entropy_range: number;

  /** Haralick idm mean */
  haralick_idm_mean: number;

  /** Haralick idm range */
  haralick_idm_range: number;

  /** Haralick imc1 mean */
  haralick_imc1_mean: number;

  /** Haralick imc1 range */
  haralick_imc1_range: number;

  /** Haralick imc2 mean */
  haralick_imc2_mean: number;

  /** Haralick imc2 range */
  haralick_imc2_range: number;

  /** Haralick sumaverage mean */
  haralick_sumaverage_mean: number;

  /** Haralick sumaverage range */
  haralick_sumaverage_range: number;

  /** Haralick sumentropy mean */
  haralick_sumentropy_mean: number;

  /** Haralick sumentropy range */
  haralick_sumentropy_range: number;

  /** Haralick sumofsquares mean */
  haralick_sumofsquares_mean: number;

  /** Haralick sumofsquares range */
  haralick_sumofsquares_range: number;

  /** Haralick sumvariance mean */
  haralick_sumvariance_mean: number;

  /** Haralick sumvariance range */
  haralick_sumvariance_range: number;

  /** Intensity histenergy */
  intensity_histenergy: number;

  /** Intensity histentropy */
  intensity_histentropy: number;

  /** Intensity iqr */
  intensity_iqr: number;

  /** Intensity kurtosis */
  intensity_kurtosis: number;

  /** Intensity mad */
  intensity_mad: number;

  /** Intensity max */
  intensity_max: number;

  /** Intensity mean */
  intensity_mean: number;

  /** Intensity meanmediandiff */
  intensity_meanmediandiff: number;

  /** Intensity median */
  intensity_median: number;

  /** Intensity min */
  intensity_min: number;

  /** Intensity skewness */
  intensity_skewness: number;

  /** Intensity std */
  intensity_std: number;

  /** Orientation */
  orientation: number;

  /** Shape circularity */
  shape_circularity: number;

  /** Shape eccentricity */
  shape_eccentricity: number;

  /** Shape equivalentdiameter */
  shape_equivalentdiameter: number;

  /** Shape extent */
  shape_extent: number;

  /** Shape fsd1 */
  shape_fsd1: number;

  /** Shape fsd2 */
  shape_fsd2: number;

  /** Shape fsd3 */
  shape_fsd3: number;

  /** Shape fsd4 */
  shape_fsd4: number;

  /** Shape fsd5 */
  shape_fsd5: number;

  /** Shape fsd6 */
  shape_fsd6: number;

  /** Shape fractaldimension */
  shape_fractaldimension: number;

  /** Shape humoments1 */
  shape_humoments1: number;

  /** Shape humoments2 */
  shape_humoments2: number;

  /** Shape humoments3 */
  shape_humoments3: number;

  /** Shape humoments4 */
  shape_humoments4: number;

  /** Shape humoments5 */
  shape_humoments5: number;

  /** Shape humoments6 */
  shape_humoments6: number;

  /** Shape humoments7 */
  shape_humoments7: number;

  /** Shape minormajoraxisratio */
  shape_minormajoraxisratio: number;

  /** Shape solidity */
  shape_solidity: number;

  /** Shape weightedhumoments1 */
  shape_weightedhumoments1: number;

  /** Shape weightedhumoments2 */
  shape_weightedhumoments2: number;

  /** Shape weightedhumoments3 */
  shape_weightedhumoments3: number;

  /** Shape weightedhumoments4 */
  shape_weightedhumoments4: number;

  /** Shape weightedhumoments5 */
  shape_weightedhumoments5: number;

  /** Shape weightedhumoments6 */
  shape_weightedhumoments6: number;

  /** Shape weightedhumoments7 */
  shape_weightedhumoments7: number;

  /** Size area */
  size_area: number;

  /** Size convexhullarea */
  size_convexhullarea: number;

  /** Size majoraxislength */
  size_majoraxislength: number;

  /** Size minoraxislength */
  size_minoraxislength: number;

  /** Size perimeter */
  size_perimeter: number;

  /** Structure type  */
  structure_type: string;

  /** Detection dataset */
  detection_dataset: number;
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
  tours: number[];
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

  /** Failure */
  failure?: string;

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
  /** id */
  id: number;

  /** investigation */
  investigation: number;

  /** parent */
  parent: number;

  /** minimum_zoom */
  minimum_zoom: number;

  /** maximum_zoom */
  maximum_zoom: number;

  /** location */
  location: string;

  /** color */
  color: string;

  /** pin_type */
  pin_type: string;

  /** description */
  description?: string;

  /** note */
  note?: string;

  /** child */
  child?: number;
}

export interface Waypoint {
  /** ID */
  id?: number;

  /** Location */
  location?: string | null;

  /**
   * Zoom
   * @min -2147483648
   * @max 2147483647
   */
  zoom?: number | null;
}

export interface Tour {
  /** ID */
  id?: number;
  waypoints: Waypoint[];

  /** Name */
  name?: string;

  /** Investigation */
  investigation: number;
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

export interface DatasetsTileSourceDataHistogramParams {
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

export interface DatasetsTileSourceDataPixelParams {
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

export interface DatasetsTileSourceRegionParams {
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

  /** Image data format (png | jpeg | tiff) */
  fmt: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceThumbnailParams {
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

  /** Image format (png | jpeg) */
  fmt: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceInfoBandParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** The band number to use. */
  band?: number;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceInfoBandsParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceInfoFramesParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceInfoMetadataParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

  /** A unique integer value identifying this dataset. */
  id: number;
}

export interface DatasetsTileSourceInfoMetadataInternalParams {
  /** The projection in which to open the image (try `EPSG:3857`). */
  projection?: string;

  /** The source to use when opening the image. Use the `large-image/sources` endpoint to list the available sources. */
  source?: string;

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

export interface DatasetsTileSourceTilesReadParams {
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

  /** Image format (png | jpeg) */
  fmt: string;

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

export interface DetectedStructuresListParams {
  /** Number of results to return per page. */
  limit?: number;

  /** The initial index from which to return the results. */
  offset?: number;
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
   * @name DatasetsTileSourceDataHistogram
   * @summary Returns histogram
   * @request GET:/datasets/tile_source/{id}/data/histogram
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceDataHistogram {
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
   * @name DatasetsTileSourceDataPixel
   * @summary Returns single pixel.
   * @request GET:/datasets/tile_source/{id}/data/pixel
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceDataPixel {
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
   * @name DatasetsTileSourceRegion
   * @summary Returns region tile binary.
   * @request GET:/datasets/tile_source/{id}/data/region.{fmt}
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceRegion {
    export type RequestParams = { fmt: string; id: number };
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
   * @name DatasetsTileSourceThumbnail
   * @summary Returns thumbnail of full image.
   * @request GET:/datasets/tile_source/{id}/data/thumbnail.{fmt}
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceThumbnail {
    export type RequestParams = { fmt: string; id: number };
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
   * @name DatasetsTileSourceInfoBand
   * @summary Returns bands information.
   * @request GET:/datasets/tile_source/{id}/info/band
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceInfoBand {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string; band?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceInfoBands
   * @summary Returns bands information.
   * @request GET:/datasets/tile_source/{id}/info/bands
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceInfoBands {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceInfoFrames
   * @summary Retrieve all channels/bands for each frame. This is used to generate a UI to control how the image is displayed.
   * @request GET:/datasets/tile_source/{id}/info/frames
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceInfoFrames {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceInfoMetadata
   * @summary Returns tile metadata.
   * @request GET:/datasets/tile_source/{id}/info/metadata
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceInfoMetadata {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceInfoMetadataInternal
   * @summary Returns additional known metadata about the tile source.
   * @request GET:/datasets/tile_source/{id}/info/metadata_internal
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceInfoMetadataInternal {
    export type RequestParams = { id: number };
    export type RequestQuery = { projection?: string; source?: string };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTileSourceInfoTiffdump
   * @summary Returns tifftools tiffdump JSON. This will raise a `ValidationError` if the image is not a Tiff.
   * @request GET:/datasets/tile_source/{id}/info/tiffdump
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceInfoTiffdump {
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
   * @name DatasetsTileSourceTilesRead
   * @summary Returns tile image binary.
   * @request GET:/datasets/tile_source/{id}/tiles/{z}/{x}/{y}.{fmt}
   * @response `200` `Dataset`
   */
  export namespace DatasetsTileSourceTilesRead {
    export type RequestParams = { fmt: string; id: number; x: number; y: number; z: number };
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

export namespace DetectedStructures {
  /**
   * No description
   * @tags detected-structures
   * @name DetectedStructuresList
   * @request GET:/detected-structures
   * @response `200` `{ count: number, next?: string | null, previous?: string | null, results: (DetectedStructure)[] }`
   */
  export namespace DetectedStructuresList {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = {
      count: number;
      next?: string | null;
      previous?: string | null;
      results: DetectedStructure[];
    };
  }
  /**
   * No description
   * @tags detected-structures
   * @name DetectedStructuresRead
   * @request GET:/detected-structures/{id}
   * @response `200` `DetectedStructure`
   */
  export namespace DetectedStructuresRead {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = DetectedStructure;
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
   * @name InvestigationsEmbeddingsRead
   * @request GET:/investigations/{id}/embeddings
   * @response `200` `(DatasetEmbedding)[]`
   */
  export namespace InvestigationsEmbeddingsRead {
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
   * @name InvestigationsPinsRead
   * @request GET:/investigations/{id}/pins
   * @response `200` `(Pin)[]`
   */
  export namespace InvestigationsPinsRead {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Pin[];
  }
  /**
   * No description
   * @tags investigations
   * @name InvestigationsTours
   * @request GET:/investigations/{id}/tours
   * @response `200` `(Tour)[]`
   */
  export namespace InvestigationsTours {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Tour[];
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
