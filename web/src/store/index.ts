import Vue from 'vue';
import Vuex from 'vuex';
import { createDirectStore } from 'direct-vuex';

import { AxiosInstance, AxiosResponse } from 'axios';
import {
  Investigation, Dataset, TileMetadata, Pin, DatasetEmbedding,
} from '../generatedTypes/AtlascopeTypes';

Vue.use(Vuex);

interface TiffFrame {
  name: string;
  frame: number;
  displayed: boolean;
  color: string;
}

export interface State {
    investigations: Investigation[];
    axiosInstance: AxiosInstance | null;
    currentInvestigation: Investigation | null;
    currentDatasets: Dataset[];
    activeDataset: Dataset | null;
    currentPins: Pin[];
    selectedPins: Pin[];
    datasetEmbeddings: DatasetEmbedding[];
    datasetTileMetadata: { [key: string]: TileMetadata };
    activeDatasetFrames: TiffFrame[];
}

interface TileMetadataForDataset {
    datasetId: string;
    tileMetadata: TileMetadata;
}

const {
  store,
  rootActionContext,
  moduleActionContext,
  rootGetterContext,
  moduleGetterContext,
} = createDirectStore({
  state: {
    investigations: [],
    axiosInstance: null,
    currentInvestigation: null,
    currentDatasets: [],
    activeDataset: null,
    currentPins: [],
    selectedPins: [],
    datasetEmbeddings: [],
    datasetTileMetadata: {},
    activeDatasetFrames: [],
  } as State,
  mutations: {
    setInvestigations(state, investigations: Investigation[]) {
      state.investigations = investigations;
    },
    setCurrentInvestigation(state, currentInvestigation: Investigation | null) {
      state.currentInvestigation = currentInvestigation;
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
    setCurrentPins(state, pins: Pin[]) {
      state.currentPins = pins;
    },
    setSelectedPins(state, pins: Pin[]) {
      state.selectedPins = pins;
    },
    setDatasetEmbeddings(state, embeddings: DatasetEmbedding[]) {
      state.datasetEmbeddings = embeddings;
    },
    setTileMetadataForDataset(state, obj: TileMetadataForDataset) {
      state.datasetTileMetadata[obj.datasetId] = obj.tileMetadata;
    },
    setActiveDatasetFrames(state, frames: TiffFrame[]) {
      state.activeDatasetFrames = frames;
    },
  },
  getters: {
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

          const embeddings: DatasetEmbedding[] = (await store.state.axiosInstance.get(`/investigations/${investigationId}/embeddings`)).data;
          commit.setDatasetEmbeddings(embeddings);

          const metadataPromises: Promise<{ datasetId: string; result: AxiosResponse }>[] = [];
          tileSourceDatasets.forEach((dataset) => {
            const promise = store.state.axiosInstance?.get(`/datasets/${dataset.id}/tiles/metadata`).then((result) => ({
              datasetId: dataset.id,
              result,
            }));
            if (promise) {
              metadataPromises.push(promise);
            }
          });
          embeddings.forEach((embedding) => {
            const promise = store.state.axiosInstance?.get(`/datasets/${embedding.child}/tiles/metadata`).then((result) => ({
              datasetId: embedding.child,
              result,
            }));
            if (promise) {
              metadataPromises.push(promise);
            }
          });
          embeddings.forEach((embedding) => {
            const promise = store.state.axiosInstance?.get(`/datasets/${embedding.parent}/tiles/metadata`).then((result) => ({
              datasetId: embedding.parent,
              result,
            }));
            if (promise) {
              metadataPromises.push(promise);
            }
          });
          const metadataResponses = await Promise.all(metadataPromises);
          metadataResponses.forEach((resp) => {
            commit.setTileMetadataForDataset({
              datasetId: resp.datasetId,
              tileMetadata: resp.result.data,
            });
          });

          const pins = (await store.state.axiosInstance.get(`/investigations/${investigationId}/pins`)).data;
          commit.setCurrentPins(pins);
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
    updateSelectedPins(context, pins: Pin[]) {
      const { commit } = rootActionContext(context);
      commit.setSelectedPins(pins);
    },
    updateFrames(context, frames: TiffFrame[]) {
      const { commit } = rootActionContext(context);
      commit.setActiveDatasetFrames(frames);
    },
    storeAxiosInstance(context, axiosInstance) {
      const { commit } = rootActionContext(context);
      commit.setAxiosInstance(axiosInstance);
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
