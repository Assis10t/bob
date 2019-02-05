<template>
    <div>
        <header>
            <div class="container">
                <nav class="navbar" role="navigation" aria-label="main navigation">
                    <div class="navbar-brand">
                        <nuxt-link class="navbar-item" to="/">
                            Bob
                        </nuxt-link>

                        <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
                            <span aria-hidden="true"></span>
                            <span aria-hidden="true"></span>
                            <span aria-hidden="true"></span>
                        </a>
                    </div>

                    <div id="navbarBasicExample" class="navbar-menu">
                        <div class="navbar-start">
                            <nuxt-link to="/" class="navbar-item">
                                Home
                            </nuxt-link>

                            <nuxt-link to="/items" class="navbar-item">
                                Items
                            </nuxt-link>
                        </div>

                        <div class="navbar-end">
                            <div class="navbar-item">
                                <div class="buttons">
                                    <nuxt-link to="/items/create" class="button is-primary">
                                        <span>
                                            <strong>Add an item</strong>
                                        </span>
                                    </nuxt-link>
                                    <nuxt-link to="/login" class="button is-light">
                                        Log in
                                    </nuxt-link>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>
            </div>
        </header>

        <nuxt />
    </div>
</template>

<style>
    
</style>
