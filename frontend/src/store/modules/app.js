const state = {
  sidebarCollapsed: false
}

const mutations = {
  TOGGLE_SIDEBAR: (state) => {
    state.sidebarCollapsed = !state.sidebarCollapsed
  }
}

const actions = {
  toggleSidebar({ commit }) {
    commit('TOGGLE_SIDEBAR')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 