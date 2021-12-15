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

  /** Source uri */
  source_uri: string;
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

  /** Datasets */
  datasets?: string;

  /** Pins */
  pins?: string;

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
   * @name UsersMe
   * @request GET:/users/me
   * @response `200` `(User)[]`
   */
  export namespace UsersMe {
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
