package io.github.assis10t.bobandroid.pojo

class Warehouse (
    val _id: String? = null,
    val name: String = "Unnamed Warehouse",
    val merchantId: String? = null,
    val location: Location? = null,
    val items: List<Item>? = null
) {
    companion object {
        class Location(
            latitude: Double = 0.0,
            longitude: Double = 0.0
        )
    }
}