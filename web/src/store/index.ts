import Vue from 'vue';
import Vuex from 'vuex';
import { createDirectStore } from 'direct-vuex';

import { User, Investigation } from '../generatedTypes/AtlascopeTypes';

Vue.use(Vuex);

export interface State {
    userInfo: User | null;
    investigations: Investigation[];
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
  } as State,
  mutations: {
    setInvestigations(state, investigations: Investigation[]) {
      state.investigations = investigations;
    },
    setUserInfo(state, userInfo: User | null) {
      state.userInfo = userInfo;
    },
  },
  actions: {
    async fetchInvestigations(context, axiosInstance) {
      const { commit } = rootActionContext(context);
      const investigations = (await axiosInstance.get('/investigations')).data;
      commit.setInvestigations(investigations.results);
    },
    async fetchUserInfo(context, axiosInstance) {
      const { commit } = rootActionContext(context);
      const userInfo = (await axiosInstance.get('/users/me')).data;
      commit.setUserInfo(userInfo);
    },
    logout(context) {
      const { commit } = rootActionContext(context);
      commit.setUserInfo(null);
      commit.setInvestigations([]);
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
