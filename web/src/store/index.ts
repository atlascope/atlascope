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
    rootDataset: Dataset | null;
    currentPins: Pin[];
    selectedPins: Pin[];
    datasetEmbeddings: DatasetEmbedding[];
    datasetTileMetadata: { [key: number]: TileMetadata };
    rootDatasetFrames: TiffFrame[];
    selectionMode: boolean;
    subimageSelection: number[] | null;
}

interface TileMetadataForDataset {
    datasetId: number;
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
    rootDataset: null,
    currentPins: [],
    selectedPins: [],
    datasetEmbeddings: [],
    datasetTileMetadata: {},
    rootDatasetFrames: [],
    selectionMode: false,
    subimageSelection: null,
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
    setRootDataset(state, dataset: Dataset | null) {
      state.rootDataset = dataset;
      state.selectionMode = false;
      state.subimageSelection = null;
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
    setRootDatasetFrames(state, frames: TiffFrame[]) {
      state.rootDatasetFrames = frames;
    },
    setSelectionMode(state, mode: boolean) {
      state.selectionMode = mode;
    },
    setSubimageSelection(state, selection: number[] | null) {
      state.subimageSelection = selection;
    },
  },
  getters: {
    tilesourceDatasets(state: State): Dataset[] {
      return state.currentDatasets.filter((dataset) => dataset.dataset_type === 'tile_source');
    },
  },
  actions: {
    async fetchInvestigations(context) {
      const { commit, state } = rootActionContext(context);
      if (state.axiosInstance) {
        const investigations = (await state.axiosInstance.get('/investigations')).data;
        commit.setInvestigations(investigations.results);
      } else {
        commit.setInvestigations([]);
      }
    },
    async fetchCurrentInvestigation(context, investigationId: string) {
      const { commit, state } = rootActionContext(context);
      if (state.axiosInstance) {
        const investigation = (await state.axiosInstance.get(`/investigations/${investigationId}`)).data;
        commit.setCurrentInvestigation(investigation);

        if (state.currentInvestigation) {
          const datasetPromises: Promise<AxiosResponse>[] = [];
          state.currentInvestigation.datasets.forEach((datasetId: string) => {
            const promise = state.axiosInstance?.get(`/datasets/${datasetId}`);
            if (promise) {
              datasetPromises.push(promise);
            }
          });
          const datasets = (await Promise.all(datasetPromises)).map((response) => response.data);
          commit.setCurrentDatasets(datasets);

          const tileSourceDatasets = datasets.filter((dataset: Dataset) => dataset.dataset_type === 'tile_source');
          const rootDataset = tileSourceDatasets.length > 0 ? tileSourceDatasets[0] : null;
          commit.setRootDataset(rootDataset);

          const embeddings: DatasetEmbedding[] = (await state.axiosInstance.get(`/investigations/${investigationId}/embeddings`)).data;
          commit.setDatasetEmbeddings(embeddings);

          const metadataPromises: Promise<{ datasetId: number; result: AxiosResponse }>[] = [];
          tileSourceDatasets.forEach((dataset) => {
            const promise = state.axiosInstance?.get(
              `/datasets/${dataset.id}/tiles/metadata`).then(
              (result: AxiosResponse) => ({
                datasetId: dataset.id,
                result,
              }));
            if (promise) {
              metadataPromises.push(promise);
            }
          });
          embeddings.forEach((embedding) => {
            const promise = state.axiosInstance?.get(
              `/datasets/${embedding.child}/tiles/metadata`).then(
                (result: AxiosResponse) => ({
                  datasetId: embedding.child,
                  result,
                }));
            if (promise) {
              metadataPromises.push(promise);
            }
          });
          embeddings.forEach((embedding) => {
            const promise = state.axiosInstance?.get(
              `/datasets/${embedding.parent}/tiles/metadata`).then(
                (result: AxiosResponse) => ({
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

          const pins = (await state.axiosInstance.get(`/investigations/${investigationId}/pins`)).data;
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
      commit.setRootDataset(null);
    },
    setRootDataset(context, dataset: Dataset | null) {
      const { commit } = rootActionContext(context);
      commit.setRootDataset(dataset);
    },
    updateSelectedPins(context, pins: Pin[]) {
      const { commit } = rootActionContext(context);
      commit.setSelectedPins(pins);
    },
    updateFrames(context, frames: TiffFrame[]) {
      const { commit } = rootActionContext(context);
      commit.setRootDatasetFrames(frames);
    },
    async createSubimageDataset(context, selection): Promise<AxiosResponse | boolean> {
      const { state } = rootActionContext(context);

      // TODO: rewrite when multiple datasets are shown
      const dataset = state.rootDataset;

      if (state.axiosInstance && dataset) {
        return (await state.axiosInstance.post(
          `/datasets/${dataset.id}/subimage`,
          {
            x0: selection[0],
            y0: selection[1],
            x1: selection[2],
            y1: selection[3],
          },
        )).data;
      }
      return false;
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
