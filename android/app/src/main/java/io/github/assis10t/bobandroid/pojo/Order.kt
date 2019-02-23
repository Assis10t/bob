package io.github.assis10t.bobandroid.pojo

class Order(
    val _id: String? = null,
    val userId: String? = null,
    val warehouseId: String? = null,
    val timestamp: String? = null,
    val items: List<Item> = listOf(),
    val status: OrderStatus = OrderStatus.PENDING
) {
    companion object {
        enum class OrderStatus {
            PENDING, IN_TRANSIT, COMPLETE, CANCELED
        }
    }
}