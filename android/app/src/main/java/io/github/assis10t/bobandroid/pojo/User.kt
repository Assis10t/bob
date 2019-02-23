package io.github.assis10t.bobandroid.pojo

import com.google.gson.annotations.SerializedName

class User (
    val _id: String? = null,
    val username: String? = null,
    val type: UserType = UserType.CUSTOMER
) {
    companion object {
        enum class UserType {
            @SerializedName("customer") CUSTOMER,
            @SerializedName("merchant") MERCHANT,
            @SerializedName("robot") ROBOT
        }
    }
}