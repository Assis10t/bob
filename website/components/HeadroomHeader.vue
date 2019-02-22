<template>
    <headroom 
        :disabled="disabled" 
        :style="[(project != undefined) ? {transform: 'none !important'} : {}]"
        :class="{'is-transparent': isActive(homepage_url), 'is-sticked': project != undefined, 'menu-open': openedMenu}"
        
        :onNotTop="showProjectInfo"
        :onTop="hideProjectInfo">
        <header>
            <nav 
                class="navbar" 
                role="navigation" aria-label="main navigation">
                <div class="navbar-brand">
                    <a class="navbar-item" :href="homepage_url">
                        <img src="~/assets/images/bob-logo-new.svg">
                    </a>

                    <transition name="slide-top" mode="out-in" v-if="project">
                        <h4 v-if="showProject" class="is-flex align-center ml20">{{ project.title }}</h4>
                    </transition>

                    <a role="button" 
                        :class="{'navbar-burger': true, 'burger': true, 'is-active': openedMenu}" 
                        aria-label="menu" aria-expanded="false" @click="toggleMenu()">
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                    </a>
                </div>

                <div id="main-nav" :class="{'navbar-menu': true, 'is-active': openedMenu}" v-cloak>
                    
                    <div class="navbar-end" v-if="!showProject" key="menu">
                        <div 
                            :class="[
                                'navbar-item',
                            ]"
                            v-for="(link, i) in links"
                            :key="link.name">

                            <nuxt-link 
                                :to="link.url" 
                                :class="[
                                    'navbar-link',
                                    {'is-active': isActive(link.url)},
                                ]">

                                {{ link.name }} 
                            </nuxt-link>    
                        </div>

                        <div class="navbar-item ml30">
                            <nuxt-link 
                                to="/login" 
                                class="button is-primary is-outlined is-smallish">

                                <span>Login</span>
                            </nuxt-link>
                        </div>

                        <div class="navbar-item">
                            <nuxt-link 
                                to="/register" 
                                class="navbar-link">

                                <span>Register</span>
                            </nuxt-link>
                        </div>

                        <div class="navbar-item">
                            <a 
                                :href="admin_route" 
                                class="navbar-link"
                                target="_blank"
                                v-if="auth">

                                <i class="mdi mdi-account is-size-4"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </nav>
        </header>
    </headroom>
</template>

<script>
import { headroom } from 'vue-headroom'

export default {
    props: ['disabled', 'logo_url' , 'links', 'recieved_project', 'social', 'auth', 'admin_route', 'flights_url'],
    components: {
        headroom
    },

    data: function () {
        return {
            openedMenu: false,
            project: undefined,
            showProject: false,
            last_expand: 0,
            expands: []
        }
    },
    methods: {
        toggleMenu: function () {
            this.openedMenu = !this.openedMenu
        },
        toggleDropdown: function (i) {
            if (this.openedMenu) {
                Vue.set(this.expands, i, !this.expands[i])
                if (this.last_expand != i) {
                    Vue.set(this.expands, this.last_expand, false)
                    this.last_expand = i
                }
            }
        },
        isActive: function (url) {
            // console.log(url, location.pathname, location.href)
            // if (url + '/' == location.href) {
            //     return true
            // }
            // return location.href == url
        },
        showProjectInfo: function () {
            if (this.project) {
                this.showProject = true
            }
        },
        hideProjectInfo: function () {
            if (this.project) {
                this.showProject = false
            }
        },
    },
    computed: {
        homepage_url: function () {
            return this.home_url ? this.home_url : this.links[0].url
        },
    },
    watch: {
        recieved_project: function (nv, ov) {
            this.project = nv ? nv : undefined
        }
    },
    mounted: function () {
        
    }
}
</script>