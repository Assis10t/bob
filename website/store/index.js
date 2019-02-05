export const strict = false

export const state = () => ({
    counter: 0,
    user: null
})
  
export const mutations = {
    increment (state) {
        state.counter++
    },
    setUser (state, payload) {
        state.user = payload
    }

    // signUpWithEmail ({commit}) {
    //     return new Promise((resolve, reject) => {
            
    //     })
    // }
}

export const actions = {

}