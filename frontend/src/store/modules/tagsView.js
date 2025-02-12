const state = {
  cachedViews: []
}

const mutations = {
  ADD_CACHED_VIEW: (state, view) => {
    if (state.cachedViews.includes(view.name)) return
    if (view.meta && view.meta.cache) {
      state.cachedViews.push(view.name)
    }
  },

  DEL_CACHED_VIEW: (state, view) => {
    const index = state.cachedViews.indexOf(view.name)
    index > -1 && state.cachedViews.splice(index, 1)
  },

  DEL_ALL_CACHED_VIEWS: state => {
    state.cachedViews = []
  }
}

const actions = {
  addCachedView({ commit }, view) {
    commit('ADD_CACHED_VIEW', view)
  },

  delCachedView({ commit }, view) {
    commit('DEL_CACHED_VIEW', view)
  },

  delAllCachedViews({ commit }) {
    commit('DEL_ALL_CACHED_VIEWS')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 