import Vue from 'vue';
import Vuex from 'vuex';
import { createDirectStore } from 'direct-vuex';

import { AxiosInstance, AxiosResponse } from 'axios';
import {
  User, Investigation, InvestigationDetail, Dataset, TileMetadata,
} from '../generatedTypes/AtlascopeTypes';
import {
  JobResults, Job,
} from '../generatedTypes/DemoTypes';

Vue.use(Vuex);

export interface State {
    userInfo: User | null;
    investigations: Investigation[];
    axiosInstance: AxiosInstance | null;
    currentInvestigation: InvestigationDetail | null;
    currentDatasets: Dataset[];
    activeDataset: Dataset | null;
    jobResults: JobResults[];
}

const jobs: Job[] = [
  {
    name: 'Brightest N Pixels',
    id: '1',
    inputs: [
      { name: 'n', type: 'number' },
    ],
    resultsType: 'text',
  },
  {
    name: 'Average Color',
    id: '2',
    resultsType: 'image',
  },
];

const jobResultList: JobResults[] = [
  {
    id: '1',
    job: jobs[0],
    status: 'running',
    updated: '1/1/2022 12:36:35',
  },
  {
    id: '2',
    job: jobs[0],
    status: 'error',
    updated: '1/7/2022 14:49:44',
  },
  {
    id: '3',
    job: jobs[0],
    status: 'success',
    updated: '1/18/2022 18:07:11',
  },
];

const {
  store,
  rootActionContext,
  moduleActionContext,
  rootGetterContext,
  moduleGetterContext,
} = createDirectStore({
  state: {
    userInfo: null,
    investigations: [],
    axiosInstance: null,
    currentInvestigation: null,
    currentDatasets: [],
    activeDataset: null,
    jobResults: jobResultList || [],
  } as State,
  mutations: {
    setInvestigations(state, investigations: Investigation[]) {
      state.investigations = investigations;
    },
    setCurrentInvestigation(state, currentInvestigation: InvestigationDetail | null) {
      state.currentInvestigation = currentInvestigation;
    },
    setUserInfo(state, userInfo: User | null) {
      state.userInfo = userInfo;
    },
    setAxiosInstance(state, axiosInstance: AxiosInstance | null) {
      state.axiosInstance = axiosInstance;
    },
    setCurrentDatasets(state, datasets: Dataset[]) {
      state.currentDatasets = datasets;
    },
    setActiveDataset(state, dataset: Dataset | null) {
      state.activeDataset = dataset;
    },
    // Demo/mock functions
    addNewJobResults(state, results: JobResults) {
      state.jobResults.push(results);
    },
  },
  getters: {
    // Demo/mock functions
    pins(state: State): any[] {
      if (state.currentInvestigation !== null) {
        // Use placeholders until GET /pins is implemented
        return [
          {
            id: 'pin_1',
            dataset: null,
            color: 'red',
            note: 'I am only a test pin.',
          },
          {
            id: 'pin_2',
            dataset: null,
            color: 'green',
            note: 'I am also just a test pin.',
          },
        ];
      }
      return [];
    },
    jobs(state: State): Job[] {
      if (state.userInfo !== null) {
        return jobs;
      }
      return [];
    },
    jobResults(state: State): JobResults[] | undefined {
      if (state.userInfo !== null) {
        return state.jobResults;
      }
      return [];
    },
    tilesourceDatasets(state: State): Dataset[] {
      return state.currentDatasets.filter((dataset) => dataset.dataset_type === 'tile_source');
    },
  },
  actions: {
    async fetchInvestigations(context) {
      const { commit } = rootActionContext(context);
      if (store.state.axiosInstance) {
        const investigations = (await store.state.axiosInstance.get('/investigations')).data;
        commit.setInvestigations(investigations.results);
      } else {
        commit.setInvestigations([]);
      }
    },
    async fetchCurrentInvestigation(context, investigationId: string) {
      const { commit } = rootActionContext(context);
      if (store.state.axiosInstance) {
        const investigation = (await store.state.axiosInstance.get(`/investigations/${investigationId}`)).data;
        commit.setCurrentInvestigation(investigation);

        if (store.state.currentInvestigation) {
          const datasetPromises: Promise<AxiosResponse>[] = [];
          store.state.currentInvestigation.datasets.forEach((datasetId) => {
            const promise = store.state.axiosInstance?.get(`/datasets/${datasetId}`);
            if (promise) {
              datasetPromises.push(promise);
            }
          });
          const datasets = (await Promise.all(datasetPromises)).map((response) => response.data);
          commit.setCurrentDatasets(datasets);

          const tileSourceDatasets = datasets.filter((dataset: Dataset) => dataset.dataset_type === 'tile_source');
          const activeDataset = tileSourceDatasets.length > 0 ? tileSourceDatasets[0] : null;
          commit.setActiveDataset(activeDataset);
        }
      } else {
        commit.setCurrentInvestigation(null);
      }
    },
    unsetCurrentInvestigation(context) {
      const { commit } = rootActionContext(context);
      commit.setCurrentInvestigation(null);
      commit.setCurrentDatasets([]);
      commit.setActiveDataset(null);
    },
    setActiveDataset(context, dataset: Dataset | null) {
      const { commit } = rootActionContext(context);
      commit.setActiveDataset(dataset);
    },
    async fetchDatasetMetadata(_context, datasetId: string): Promise<TileMetadata | null> {
      if (store.state.axiosInstance) {
        const url = `/datasets/${datasetId}/tiles/metadata`;
        const metadata = (await store.state.axiosInstance.get(url)).data;
        return metadata;
      }
      return null;
    },
    async fetchUserInfo(context) {
      const { commit } = rootActionContext(context);
      if (store.state.axiosInstance) {
        const userInfo = (await store.state.axiosInstance.get('/users/me')).data;
        commit.setUserInfo(userInfo);
      }
    },
    logout(context) {
      const { commit } = rootActionContext(context);
      commit.setUserInfo(null);
      commit.setInvestigations([]);
    },
    storeAxiosInstance(context, axiosInstance) {
      const { commit } = rootActionContext(context);
      commit.setAxiosInstance(axiosInstance);
    },

    // Demo/mock functions
    addJobResults(context, results: JobResults) {
      const { commit } = rootActionContext(context);
      commit.addNewJobResults(results);
    },
  },
});

export default store;
export {
  rootActionContext,
  moduleActionContext,
  rootGetterContext,
  moduleGetterContext,
};

// Enable types in injected $store
export type ApplicationStore = typeof store;
declare module 'vuex' {
    interface Store<S> {
        direct: ApplicationStore;
    }
}
