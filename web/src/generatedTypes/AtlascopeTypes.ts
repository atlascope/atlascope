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

  /** Public */
  public?: boolean;

  /**
   * Content
   * @format uri
   */
  content?: string | null;

  /** Extension */
  extension?: string;

  /** Metadata */
  metadata?: object | null;

  /** Dataset type */
  dataset_type?: "tile_source" | "tile_overlay" | "analytics";
  derived_datasets?: string[];
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

  /** Owner */
  owner?: string;
}

export interface InvestigationDetail {
  /**
   * Id
   * @format uuid
   */
  id?: string;

  /** Owner */
  owner?: string;

  /** Investigators */
  investigators?: string;

  /** Observers */
  observers?: string;

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

  /** Name */
  name: string;

  /** Description */
  description?: string;

  /** Notes */
  notes?: string;
  datasets: string[];
  pins: string[];
}

export interface Job {
  /**
   * Id
   * @format uuid
   */
  id?: string;

  /**
   * Input image
   * @format uri
   */
  input_image?: string | null;

  /** Other inputs */
  other_inputs?: object | null;

  /** Outputs */
  outputs?: object | null;

  /**
   * Last run
   * @format date-time
   */
  last_run?: string | null;

  /**
   * Preview visual
   * @format uri
   */
  preview_visual?: string | null;

  /**
   * Script
   * @format uuid
   */
  script: string;
}

export interface JobSpawn {
  /** Input image */
  input_image: string;

  /** Other inputs */
  other_inputs?: object | null;

  /**
   * Script
   * @format uuid
   */
  script: string;
}

export interface JobScript {
  /**
   * Id
   * @format uuid
   */
  id?: string;

  /** Name */
  name: string;
}

export interface User {
  /** ID */
  id?: number;

  /**
   * Username
   * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
   * @pattern ^[\w.@+-]+$
   */
  username: string;

  /**
   * Email address
   * @format email
   */
  email?: string;

  /** First name */
  first_name?: string;

  /** Last name */
  last_name?: string;
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

export interface InvestigationsPermissionsPayload {
  /** the username of the owner of this investigation */
  owner?: string;

  /** a list of the usernames of users who should have only read access on this investigation */
  observers?: string[];

  /** a list of the usernames of users who should have write access on this investigation */
  investigators?: string[];
}

export interface JobsListParams {
  /** Number of results to return per page. */
  limit?: number;

  /** The initial index from which to return the results. */
  offset?: number;
}

export interface JobScriptsListParams {
  /** Number of results to return per page. */
  limit?: number;

  /** The initial index from which to return the results. */
  offset?: number;
}

export interface UsersListParams {
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
   * @name DatasetsPerformImport
   * @request POST:/datasets/{id}/import
   * @response `204` `void` Import successful.
   */
  export namespace DatasetsPerformImport {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = void;
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
   * @response `200` `InvestigationDetail`
   */
  export namespace InvestigationsRead {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = InvestigationDetail;
  }
  /**
   * @description Update the lists of users that have permissions on this Investigation.
   * @tags investigations
   * @name InvestigationsPermissions
   * @request POST:/investigations/{id}/permissions
   * @response `200` `InvestigationDetail`
   */
  export namespace InvestigationsPermissions {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = InvestigationsPermissionsPayload;
    export type RequestHeaders = {};
    export type ResponseBody = InvestigationDetail;
  }
}

export namespace Jobs {
  /**
   * No description
   * @tags job-runs
   * @name JobsList
   * @request GET:/job-runs
   * @response `200` `{ count: number, next?: string | null, previous?: string | null, results: (Job)[] }`
   */
  export namespace JobsList {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = { count: number; next?: string | null; previous?: string | null; results: Job[] };
  }
  /**
   * No description
   * @tags job-runs
   * @name JobsSpawn
   * @request POST:/job-runs/spawn
   * @response `201` `JobSpawn`
   */
  export namespace JobsSpawn {
    export type RequestParams = {};
    export type RequestQuery = {};
    export type RequestBody = JobSpawn;
    export type RequestHeaders = {};
    export type ResponseBody = JobSpawn;
  }
  /**
   * No description
   * @tags job-runs
   * @name JobsRead
   * @request GET:/job-runs/{id}
   * @response `200` `Job`
   */
  export namespace JobsRead {
    export type RequestParams = { id: string };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = Job;
  }
  /**
   * No description
   * @tags job-runs
   * @name JobsRerun
   * @request POST:/job-runs/{id}/rerun
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

export namespace JobScripts {
  /**
   * No description
   * @tags job-scripts
   * @name JobScriptsList
   * @request GET:/job-scripts
   * @response `200` `{ count: number, next?: string | null, previous?: string | null, results: (JobScript)[] }`
   */
  export namespace JobScriptsList {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = { count: number; next?: string | null; previous?: string | null; results: JobScript[] };
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

export namespace Users {
  /**
   * No description
   * @tags users
   * @name UsersList
   * @request GET:/users
   * @response `200` `{ count: number, next?: string | null, previous?: string | null, results: (User)[] }`
   */
  export namespace UsersList {
    export type RequestParams = {};
    export type RequestQuery = { limit?: number; offset?: number };
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = { count: number; next?: string | null; previous?: string | null; results: User[] };
  }
  /**
   * @description Return the currently logged in user's information.
   * @tags users
   * @name UsersMeRead
   * @request GET:/users/me
   * @response `200` `(User)[]`
   */
  export namespace UsersMeRead {
    export type RequestParams = {};
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = User[];
  }
  /**
   * No description
   * @tags users
   * @name UsersRead
   * @request GET:/users/{id}
   * @response `200` `User`
   */
  export namespace UsersRead {
    export type RequestParams = { id: number };
    export type RequestQuery = {};
    export type RequestBody = never;
    export type RequestHeaders = {};
    export type ResponseBody = User;
  }
}
