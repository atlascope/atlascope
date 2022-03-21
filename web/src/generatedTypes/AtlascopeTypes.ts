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
  /**
   * Id
   * @format uuid
   */
  id?: string;

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

  /**
   * Source dataset
   * @format uuid
   */
  source_dataset?: string | null;
  derived_datasets: string[];
  child_embeddings: string[];
  parent_embeddings: string[];
  jobs: string[];
  origin: string[];
  pins: string[];
  locations: string[];
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

export interface DatasetEmbedding {
  /**
   * Id
   * @format uuid
   */
  id?: string;
  child_bounding_box?: number[];

  /**
   * Investigation
   * @format uuid
   */
  investigation: string;

  /**
   * Parent
   * @format uuid
   */
  parent: string;

  /**
   * Child
   * @format uuid
   */
  child: string;
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
  /**
   * Id
   * @format uuid
   */
  id?: string;

  /** Name */
  name: string;

  /** Description */
  description?: string;
  datasets: string[];
  pins: string[];

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
  embeddings: string[];
  jobs: string[];
}

export interface DatasetEmbedding {
  /**
   * Id
   * @format uuid
   */
  id?: string;
  child_bounding_box?: number[];

  /**
   * Investigation
   * @format uuid
   */
  investigation: string;

  /**
   * Parent
   * @format uuid
   */
  parent: string;

  /**
   * Child
   * @format uuid
   */
  child: string;
}

export interface JobDetail {
  /**
   * Id
   * @format uuid
   */
  id?: string;

  /** Complete */
  complete?: boolean;

  /** Job type */
  job_type?: string;

  /** Additional inputs */
  additional_inputs?: object | null;

  /**
   * Investigation
   * @format uuid
   */
  investigation: string;

  /**
   * Original dataset
   * @format uuid
   */
  original_dataset: string;
  resulting_datasets: string[];
}

export interface Pin {
  /**
   * Id
   * @format uuid
   */
  id?: string;

  /** Child location */
  child_location: string;

  /** Color */
  color?: "red" | "blue" | "green" | "orange" | "purple" | "black";

  /** Note */
  note?: string;

  /**
   * Investigation
   * @format uuid
   */
  investigation: string;

  /**
   * Parent
   * @format uuid
   */
  parent: string;

  /**
   * Child
   * @format uuid
   */
  child?: string | null;
}

export interface JobSpawn {
  /**
   * Investigation
   * @format uuid
   */
  investigation: string;

  /** Job type */
  job_type?: string;

  /**
   * Original dataset
   * @format uuid
   */
  original_dataset: string;

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
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Dataset;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsEmbeddings
   * @request GET:/datasets/{id}/embeddings
   * @response `200` `(DatasetEmbedding)[]`
   */
  export namespace DatasetsEmbeddings {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = DatasetEmbedding[];
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsSubimage
   * @request POST:/datasets/{id}/subimage
   * @response `201` `DatasetSubImage`
   */
  export namespace DatasetsSubimage {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = DatasetSubImage;
    export type RequestHeaders = {};
    export type ResponseBody = DatasetSubImage;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTilesMetadataRead
   * @request GET:/datasets/{id}/tiles/metadata
   * @response `200` `TileMetadata`
   */
  export namespace DatasetsTilesMetadataRead {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = TileMetadata;
  }
  /**
   * No description
   * @tags datasets
   * @name DatasetsTilesRead
   * @request GET:/datasets/{id}/tiles/{z}/{x}/{y}.png
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
    export type RequestParams = { id: string };
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
    export type RequestParams = { id: string };
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
    export type RequestParams = { id: string };
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
    export type RequestParams = { id: string };
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
    export type RequestParams = { id: string };
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
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = void;
  }
}

export namespace S3Upload {
  /**
   * No description
   * @tags s3-upload
   * @name S3UploadFinalizeCreate
   * @request POST:/s3-upload/finalize/
   * @response `201` `void`
   */
  export namespace S3UploadFinalizeCreate {
    export type RequestParams = {};
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = void;
  }
  /**
   * No description
   * @tags s3-upload
   * @name S3UploadUploadCompleteCreate
   * @request POST:/s3-upload/upload-complete/
   * @response `201` `void`
   */
  export namespace S3UploadUploadCompleteCreate {
    export type RequestParams = {};
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = void;
  }
  /**
   * No description
   * @tags s3-upload
   * @name S3UploadUploadInitializeCreate
   * @request POST:/s3-upload/upload-initialize/
   * @response `201` `void`
   */
  export namespace S3UploadUploadInitializeCreate {
    export type RequestParams = {};
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = void;
  }
}
