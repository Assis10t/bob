<template>
    <div>
        <section class="section pt60 pt30t pb0">
            <div class="container has-text-centered">
                <h1 class="is-inline-block is-relative mb25">
                    Add an item to {{ warehouse.name }}
                </h1>
            </div>
        </section>

        <section class="section">
            <div class="container is-flex justify-center">
                <div class="half-width">
                    <nuxt-link to="/merchant/items" class="is-inline-block mb15">Back to all items</nuxt-link>

                    <div class="box p30 pl50 pr50">
                        <form action="">
                            <div class="field">
                                <label class="label">* Item name:</label>
                                <div class="control">
                                    <input class="input" type="text" placeholder="Enter item name" v-model="name">
                                </div>
                            </div>
                            <div class="field">
                                <label class="label">Image:</label>
                                <div class="control">
                                    <input class="input" type="file" placeholder="Enter your warehouse name" @change="uploadFile">
                                </div>
                                <img class="small-img mt15" :src="image" alt="">
                            </div>
                            <div class="field" v-if="warehouse.dimensions">
                                <label class="label">Position:</label>
                                <p class="help is-size-8">
                                    X and Y specify the row and column respectively and Z specifies which shelf the product will be on.
                                </p>
                                <div class="control columns">
                                    <div class="column is-4">
                                        <select 
                                            name="x" 
                                            id="x" 
                                            class="input"
                                            v-model.number="position.x">
                                            <option 
                                                :value="n - 1"
                                                v-for="n in (warehouse.dimensions.x + 1)">
                                                {{ n }}
                                            </option>
                                        </select>
                                    </div>
                                    <div class="column is-4">
                                        <select 
                                            name="y" 
                                            id="y" 
                                            class="input"
                                            v-model.number="position.y">
                                            <option 
                                                :value="n - 1"
                                                v-for="n in (warehouse.dimensions.y + 1)">
                                                {{ n }}
                                            </option>
                                        </select>
                                    </div>
                                    <div class="column is-4">
                                        <select 
                                            name="x" 
                                            id="x" 
                                            class="input"
                                            v-model.number="position.z">
                                            <option 
                                                :value="i"
                                                v-for="(height, i) in warehouse.dimensions.z">
                                                {{ i + 1 }}: {{ height }}m
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="field" v-if="warehouse.dimensions">
                                <div class="control columns">
                                    <div class="column is-6">
                                        <label class="label">* Quantity:</label>
                                        <input class="input" type="number" placeholder="Enter item quantity" v-model.number="quantity">
                                    </div>
                                    <div class="column is-6">
                                        <label class="label">Unit:</label>
                                        <input class="input" type="text" placeholder="Enter measurment unit" v-model="unit">
                                        <p class="help is-size-8 mb0">
                                            <i>kg</i>, <i>lbs</i>, <i>litres</i>, etc... or blank.
                                        </p>
                                    </div>
                                </div>
                            </div>
                            <div class="field">
                                <div class="control">
                                    <label class="label">Size:</label>
                                    <p class="help is-size-8">
                                        <i>Tiny</i> - 3 of these can fit in the robots basket, <i>Small</i> - 2 can fit, <i>Large</i> - 1 can fit.
                                    </p>
                                    <select 
                                        name="size" 
                                        id="size" 
                                        class="input"
                                        v-model="size">
                                        
                                        <option value="tiny">Tiny</option>
                                        <option value="small">Small</option>
                                        <option value="large">Large</option>
                                    </select>
                                </div>
                            </div>
                            <div class="field">
                                <div class="control">
                                    <label class="label">* Price (in GBP):</label>
                                    <input class="input" type="number" placeholder="Enter item price" v-model.number="price">
                                </div>
                            </div>
                            
                            <div class="field">
                                <div class="control pt30">
                                    <a 
                                        href="javascript:;"
                                        class="button is-link" 
                                        :disabled="!can_submit"
                                        @click.stop.prevent="addItem()">
                                        <span>Add item</span>
                                    </a>
                                </div>
                            </div>
                        </form>
                    </div>

                    <nuxt-link to="/merchant/items" class="is-inline-block">Back to all items</nuxt-link>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import PageTitle from '~/components/PageTitle'
import axios from 'axios'

export default {
    components: {
        PageTitle
    },
    data: function () {
        return {
            warehouseId: this.$nuxt._route.params.id,
            warehouse: {},

            name: "",
            image: null,
            position: {
                x: 0,
                y: 0,
                z: 0,
            },
            quantity: "",
            unit: null,
            size: 'tiny',
            price: ""
        }
    },
    methods: {
        getWarehouse () {
            axios.
                get(process.env.baseUrl + '/api/warehouse/' + this.warehouseId, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then((res) => {
                    console.log("Server response: ", res);
                    
                    this.warehouse = res.data.warehouse
                })
                .catch(function(error) {
                    console.error("Error adding document: ", error);
                });
        },
        uploadFile: function (event) {
            let file = event.target.files[0]
            this.createImage(file);
        },
        createImage(file) {
            var image = new Image();
            var reader = new FileReader();

            reader.onload = (e) => {
                this.image = e.target.result;
            };

            reader.readAsDataURL(file);
        },
        addItem () {
            if (this.can_submit) {
                axios.
                    post(process.env.baseUrl + '/api/warehouse/' + this.warehouseId + '/items', {
                        name: this.name,
                        image: this.image,
                        position: this.position,
                        quantity: this.quantity,
                        unit: this.unit,
                        size: this.size,
                        price: this.price,
                    }, {
                        headers: {
                            'Content-Type': 'application/json',
                            'username': this.$store.state.user.username,
                        }
                    })
                    .then((res) => {
                        console.log("Server response: ", res);
    
                        if (res.status == 200) {
                            this.$router.push('/merchant/warehouses/' + this.warehouseId).go(1)
                        }
                    })
                    .catch(function(error) {
                        console.error("Error adding document: ", error);
                    });
            }
        }
    },
    computed: {
        can_submit: function () {
            return this.name.toString().length > 0 && this.quantity.toString().length > 0 && this.price.toString().length > 0
        }
    },
    mounted: function () {
        this.getWarehouse()
    }
};
</script>

<style lang="sass" scoped>


</style>
