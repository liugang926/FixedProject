import { createStore } from 'vuex'
import user from './modules/user'
import app from './modules/app'
import permission from './modules/permission'
import tagsView from './modules/tagsView'

export default createStore({
  modules: {
    user,
    app,
    permission,
    tagsView
  }
}) 