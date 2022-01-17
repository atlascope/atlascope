import Vue from 'vue';
import Vuex from 'vuex';
import { createDirectStore } from 'direct-vuex';

import { AxiosInstance } from 'axios';
import { User, Investigation } from '../generatedTypes/AtlascopeTypes';

Vue.use(Vuex);

export interface State {
    userInfo: User | null;
    investigations: Investigation[];
    axiosInstance: AxiosInstance | null;
    currentInvestigation: Investigation | null;
}

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
  } as State,
  mutations: {
    setInvestigations(state, investigations: Investigation[]) {
      state.investigations = investigations;
    },
    setCurrentInvestigation(state, currentInvestigation: Investigation | null) {
      state.currentInvestigation = currentInvestigation;
    },
    setUserInfo(state, userInfo: User | null) {
      state.userInfo = userInfo;
    },
    setAxiosInstance(state, axiosInstance: AxiosInstance | null) {
      state.axiosInstance = axiosInstance;
    },
  },
  getters: {
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
    }
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
      } else {
        commit.setCurrentInvestigation(null);
      }
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
    unsetCurrentInvestigation(context) {
      const { commit } = rootActionContext(context);
      commit.setCurrentInvestigation(null);
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
