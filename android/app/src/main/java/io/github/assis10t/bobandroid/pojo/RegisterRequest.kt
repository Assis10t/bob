package io.github.assis10t.bobandroid.pojo

class RegisterRequest (
    val username: String,
    val type: User.Companion.UserType = User.Companion.UserType.CUSTOMER
)