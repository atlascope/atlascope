import Vue from 'vue';
import Vuex from 'vuex';
import { createDirectStore } from 'direct-vuex';

import { AxiosInstance, AxiosResponse } from 'axios';
import { nucleiToNearestGlandDistances, NucleusGlandDistance } from '@/utilities/utiltyFunctions';
import { VisOption } from '@/utilities/visualizationTypes';
import {
  Investigation, Dataset, Pin, DatasetEmbedding, JobDetail, DetectedStructure, Tour, Waypoint,
} from '../generatedTypes/AtlascopeTypes';
import { GeoBounds, GeoJSLayer } from '../utilities/composableTypes';

Vue.use(Vuex);

export interface TiffFrame {
  name: string;
  frame: number;
  displayed: boolean;
  color: string;
}

export interface TileMetadata {
  levels: number;
  size_x: number;
  size_y: number;
  tile_size: number;
  additional_metadata: object;
}

export interface State {
    investigations: Investigation[];
    axiosInstance: AxiosInstance | null;
    currentInvestigation: Investigation | null;
    currentDatasets: Dataset[];
    rootDataset: Dataset | null;
    currentPins: Pin[];
    inBoundsPins: Pin[];
    selectedPins: Pin[];
    selectedVisualizations: Dataset[];
    detectedStuctures: DetectedStructure[];
    nucleiToNearestGlandDistances: NucleusGlandDistance[];
    datasetEmbeddings: DatasetEmbedding[];
    showEmbeddings: boolean;
    datasetTileMetadata: { [key: string]: TileMetadata };
    rootDatasetFrames: TiffFrame[];
    selectionMode: boolean;
    subimageSelection: number[] | null;
    jobTypes: JobDetail[];
    currentBounds: GeoBounds;
    zoomLevel: number;
    tours: Tour[];
    selectedTour: Tour;
    selectedWaypoint: Waypoint;
    visualizationsShown: VisOption[];
    visualizationLayer: GeoJSLayer | undefined;
}

interface TileMetadataForDataset {
    datasetId: number | undefined;
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
    inBoundsPins: [],
    selectedPins: [],
    selectedVisualizations: [],
    detectedStuctures: [],
    nucleiToNearestGlandDistances: [],
    showEmbeddings: true,
    datasetEmbeddings: [],
    datasetTileMetadata: {},
    rootDatasetFrames: [],
    selectionMode: false,
    subimageSelection: null,
    jobTypes: [],
    currentBounds: {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0,
    },
    zoomLevel: 0,
    tours: [],
    selectedTour: {} as Tour,
    selectedWaypoint: {},
    visualizationsShown: [],
    visualizationLayer: undefined,
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
    resetRootDataset(state) {
      const tileSourceDatasets = state.currentDatasets.filter((dataset: Dataset) => dataset.dataset_type === 'tile_source');
      const rootDataset = tileSourceDatasets.length > 0 ? tileSourceDatasets[0] : null;
      state.rootDataset = rootDataset;
      state.selectionMode = false;
      state.subimageSelection = null;
    },
    setCurrentPins(state, pins: Pin[]) {
      state.currentPins = pins;
    },
    setSelectedPins(state, pins: Pin[]) {
      state.selectedPins = pins;
    },
    setSelectedVisualizations(state, visualizations) {
      state.selectedVisualizations = visualizations;
    },
    setTours(state, tours: Tour[]) {
      state.tours = tours;
    },
    setSelectedTour(state, tours: Tour) {
      state.selectedTour = tours;
    },
    setSelectedWaypoint(state, waypoint: Waypoint) {
      state.selectedWaypoint = waypoint;
    },
    setDatasetEmbeddings(state, embeddings: DatasetEmbedding[]) {
      state.datasetEmbeddings = embeddings;
    },
    setShowEmbeddings(state, show: boolean) {
      state.showEmbeddings = show;
    },
    setDetectedStructures(state, structures) {
      state.detectedStuctures = structures;
      state.nucleiToNearestGlandDistances = nucleiToNearestGlandDistances(structures);
    },
    setTileMetadataForDataset(state, obj: TileMetadataForDataset) {
      if (obj.datasetId) state.datasetTileMetadata[obj.datasetId] = obj.tileMetadata;
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
    setJobTypes(state, jobTypes) {
      state.jobTypes = jobTypes;
    },
    setBounds(state, newBounds: GeoBounds) {
      state.currentBounds = newBounds;
    },
    setZoomLevel(state, zoomLevel: number) {
      state.zoomLevel = zoomLevel;
    },
    setVisualizationLayer(state, layer: GeoJSLayer | undefined) {
      state.visualizationLayer = layer;
    },
    updateVisualizationsShown(state, visOption: VisOption) {
      if (state.visualizationsShown.map((vis) => vis.value).includes(visOption.value)) {
        state.visualizationsShown = state.visualizationsShown.filter(
          (vis) => vis.value !== visOption.value,
        );
      } else {
        state.visualizationsShown.push(visOption);
      }
    },
    updateVisualizationOption(state, visOption: VisOption) {
      state.visualizationsShown[
        state.visualizationsShown.findIndex((vis) => vis.value === visOption.value)
      ] = visOption;
    },
  },
  getters: {
    tilesourceDatasets(state: State): Dataset[] {
      return state.currentDatasets.filter((dataset) => dataset.dataset_type === 'tile_source');
    },
    subimageDatasets(state: State): Dataset[] {
      return state.currentDatasets.filter((dataset) => dataset.dataset_type === 'subimage');
    },
    nonTiledImageDatasets(state: State): Dataset[] {
      return state.currentDatasets.filter((dataset) => dataset.dataset_type === 'non_tiled_image');
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
      const {
        commit,
        state,
        dispatch,
        getters,
      } = rootActionContext(context);
      if (state.axiosInstance) {
        const investigation = (await state.axiosInstance.get(`/investigations/${investigationId}`)).data;
        commit.setCurrentInvestigation(investigation);

        if (state.currentInvestigation) {
          const datasetPromises: Promise<AxiosResponse>[] = [];
          state.currentInvestigation.datasets.forEach((datasetId: number) => {
            const promise = state.axiosInstance?.get(`/datasets/${datasetId}`);
            if (promise) {
              datasetPromises.push(promise);
            }
          });
          const datasets = (await Promise.all(datasetPromises)).map((response) => response.data);
          commit.setCurrentDatasets(datasets);
          commit.resetRootDataset();

          const embeddings: DatasetEmbedding[] = (await state.axiosInstance.get(`/investigations/${investigationId}/embeddings`)).data;
          commit.setDatasetEmbeddings(embeddings);

          const metadataPromises: Promise<void | {
            datasetId: number | undefined;
            result: AxiosResponse;
          }>[] = [];
          getters.tilesourceDatasets.forEach((dataset) => {
            const promise = state.axiosInstance?.get(
              `/datasets/tile_source/${dataset.id}/tiles/metadata`).then(
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
              `/datasets/tile_source/${embedding.child}/tiles/metadata`).then(
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
              `/datasets/tile_source/${embedding.parent}/tiles/metadata`).then(
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
            if (resp) {
              commit.setTileMetadataForDataset({
                datasetId: resp.datasetId,
                tileMetadata: resp.result.data,
              });
            }
          });

          await dispatch.fetchInvestigationPins();
          await dispatch.fetchInvestigationTours();
        }
      } else {
        commit.setCurrentInvestigation(null);
      }
    },
    async fetchInvestigationPins(context) {
      const { commit, state } = rootActionContext(context);
      if (state.axiosInstance && state.currentInvestigation) {
        const pins = (await state.axiosInstance.get(`/investigations/${state.currentInvestigation.id}/pins`)).data;
        commit.setCurrentPins(pins);
      }
    },
    async fetchDetectedStructures(context) {
      const { commit, state } = rootActionContext(context);
      if (state.axiosInstance) {
        commit.setDetectedStructures(
          (await state.axiosInstance.get('/detected-structures')).data,
        );
      }
    },
    async fetchInvestigationTours(context) {
      const { commit, state } = rootActionContext(context);
      if (state.axiosInstance && state.currentInvestigation) {
        const tours = (await state.axiosInstance.get(`/investigations/${state.currentInvestigation.id}/tours`)).data;
        commit.setTours(tours);
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
      const circlePinDatasetTypes = [
        'tile_overlay',
        'non_tiled_image',
        '3d_volume',
      ];
      const isVisualization: Array<boolean | Dataset> = pins.map((pin: Pin) => {
        const childDataset: Dataset | undefined = store.state.currentDatasets.find(
          (dataset: Dataset) => dataset.id === pin.child,
        );
        if (childDataset
          && childDataset?.dataset_type
          && !circlePinDatasetTypes.includes(childDataset.dataset_type)) {
          return childDataset;
        }
        return false;
      });
      const circlePins = pins.filter((pin: Pin, index: number) => !isVisualization[index]);
      const visualizations = isVisualization.filter((vis) => vis !== false);

      commit.setSelectedPins(circlePins);
      commit.setSelectedVisualizations(visualizations);
    },
    updateFrames(context, frames: TiffFrame[]) {
      const { commit } = rootActionContext(context);
      commit.setRootDatasetFrames(frames);
    },
    async createSubimageDataset(context, selection): Promise<Dataset | undefined> {
      const { state, commit } = rootActionContext(context);
      const dataset = state.rootDataset;
      const investigation = state.currentInvestigation;

      if (state.axiosInstance && dataset) {
        const response = (await state.axiosInstance.post(
          `/datasets/${dataset.id}/subimage`,
          {
            x0: selection[0],
            y0: selection[1],
            x1: selection[2],
            y1: selection[3],
            investigation: investigation?.id,
          },
        )).data;
        if (response) {
          const metadata = (await state.axiosInstance.get(
            `/datasets/tile_source/${response.id}/tiles/metadata`,
          )).data;
          commit.setTileMetadataForDataset({
            datasetId: response.id,
            tileMetadata: metadata,
          });
        }
        return response;
      }
      return undefined;
    },
    async fetchJobTypes(context) {
      const { state, commit } = rootActionContext(context);
      if (state.axiosInstance) {
        const response = (await state.axiosInstance.get('/jobs/types')).data;
        commit.setJobTypes(response);
      }
    },
    storeAxiosInstance(context, axiosInstance) {
      const { commit } = rootActionContext(context);
      commit.setAxiosInstance(axiosInstance);
    },
    setBounds(context, newBounds: GeoBounds) {
      const { commit } = rootActionContext(context);
      commit.setBounds(newBounds);
    },
    setZoom(context, zoomLevel: number) {
      const { commit } = rootActionContext(context);
      commit.setZoomLevel(zoomLevel);
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
