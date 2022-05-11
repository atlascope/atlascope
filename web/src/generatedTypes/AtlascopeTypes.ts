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
  dataset_type?: "tile_source" | "tile_overlay" | "analytics" | "subimage";

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
  dataset_type?: "tile_source" | "tile_overlay" | "analytics" | "subimage";

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

export interface TileMetadata {
  /**
   * Levels
   * Number of zoom levels in the image.
   * @min 1
   */
  levels?: number;

  /**
   * Size x
   * Image size in the X direction.
   * @min 1
   */
  size_x?: number;

  /**
   * Size y
   * Image size in the Y direction.
   * @min 1
   */
  size_y?: number;

  /**
   * Tile size
   * Size of the square tiles the image is composed of.
   * @min 1
   */
  tile_size?: number;

  /**
   * Additional metadata
   * Any additional metadata on the tile source.
   */
  additional_metadata?: object;
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
  /**
   * No description
   * @tags datasets
   * @name DatasetsTilesMetadataRead
   * @request GET:/datasets/tile_source/{id}/tiles/metadata
   * @response `200` `TileMetadata`
   */
  export namespace DatasetsTilesMetadataRead {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = TileMetadata;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTilesRead
   * @request GET:/datasets/tile_source/{id}/tiles/{z}/{x}/{y}.png
   * @response `200` `void` Image file
   * @response `404` `void` Image tile not found
   */
  export namespace DatasetsTilesRead {
    export type RequestParams = { id: string; x: number; y: number; z: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = void;
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
