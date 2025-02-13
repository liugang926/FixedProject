const getDefaultState = () => {
  return {
    sidebar: {
      opened: true
    }
  }
}

const state = getDefaultState()

const mutations = {
  TOGGLE_SIDEBAR: state => {
    state.sidebar.opened = !state.sidebar.opened
  },
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  }
}

const actions = {
  toggleSideBar({ commit }) {
    commit('TOGGLE_SIDEBAR')
  },
  
  // 添加重置状态的 action
  resetState({ commit }) {
    return new Promise(resolve => {
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 