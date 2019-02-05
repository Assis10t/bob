<template>
    <section class="is-medium is-full-height">
        <div class="container is-flex justify-center align-center is-full-height">
            <div class="box is-full-width">
                <table class="table is-full-width">
                    <thead>
                        <tr>
                            <td class="quarter-width">Item name</td>
                            <td>Quantity</td>
                            <td>Shelf</td>
                            <td>View details</td>
                            <td>Edit item</td>
                            <td>Delete item</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in items" :key="item.id">
                            <td>
                                <b>{{ item.name }}</b>
                            </td>
                            <td>
                                {{ item.qty }}
                            </td>
                            <td>
                                {{ item.shelf }}
                            </td>
                            <td>
                                <a href="#" class="has-text-info">
                                    <i class="mdi mdi-eye"></i>
                                    View
                                </a>
                            </td>
                            <td>
                                <a href="#" class="has-text-success">
                                    <i class="mdi mdi-pencil"></i>
                                    Edit
                                </a>
                            </td>
                            <td>
                                <a href="#" class="has-text-danger">
                                    <i class="mdi mdi-delete"></i>
                                    Delete
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</template>

<script>
import firebase, {auth} from '~/services/fireinit'

export default {
    data: function () {
        return {
            items: []
        }
    },
    methods: {
        getItems: function () {
            firebase.firestore().collection("items").get().then((querySnapshot) => {
                this.items = []
                querySnapshot.forEach((doc) => {
                    let item = doc.data()
                    item._id = doc.id
                    this.items.push(item)
                });
            });
        }
    },
    mounted: function () {
        this.getItems()
    }
};
</script>

<style lang="sass" scoped>

    // .box
    //     width: 32rem    

</style>
