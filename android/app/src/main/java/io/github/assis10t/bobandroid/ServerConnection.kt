package io.github.assis10t.bobandroid

import com.google.gson.Gson
import io.github.assis10t.bobandroid.pojo.GetItemsResponse
import io.github.assis10t.bobandroid.pojo.Item
import okhttp3.OkHttpClient
import okhttp3.Request
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import timber.log.Timber
import java.io.IOException
import java.util.concurrent.TimeUnit
import javax.jmdns.JmDNS
import javax.jmdns.ServiceEvent
import javax.jmdns.ServiceListener

class ServerConnection {
    companion object {
        val SERVER_NAME = "assis10t"
        var serverAddress: String? = null
        val httpClient: OkHttpClient = OkHttpClient()

        val onConnectedListeners: MutableList<(serverAddress: String) -> Unit> = mutableListOf()

        fun initialize() {
            doAsync {
                Timber.d("Discovery started")
                val mJmDNS = JmDNS.create()
                mJmDNS.addServiceListener("_http._tcp.local.", object : ServiceListener {

                    override fun serviceResolved(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Timber.d("Service resolved: $info")
                        if (info.name.contains(SERVER_NAME)) {
                            uiThread {
                                serverAddress = "http://${info.inet4Addresses[0]!!.hostAddress}:${info.port}"
                                onConnectedListeners.forEach { it(serverAddress!!) }
                                onConnectedListeners.clear()
                            }
                        }
                    }

                    override fun serviceRemoved(event: ServiceEvent?) {
                        Timber.d("Service removed")
                    }

                    override fun serviceAdded(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Timber.d("Service added: $info")
                    }
                })
            }
            ServerConnection().connect { ip ->
                Timber.d("Server found at $ip")
            }
        }
    }

    fun connect(onConnected: (String) -> Unit) {
        if (serverAddress != null)
            onConnected(serverAddress!!)
        else
            onConnectedListeners.add(onConnected)
    }

    val getRequestFactory = { http: OkHttpClient ->
        { url: String, onGetComplete: (success: Boolean, response: String?) -> Unit ->
            doAsync {
                Timber.d("Get request to $url")
                try {
                    val request = Request.Builder().url(url).build()
                    val response = http.newCall(request).execute()
                    Timber.d("Response received.")
                    if (!response.isSuccessful) {
                        Timber.e("Get Request failed: (${response.code()}) ${response.body().toString()}")
                        uiThread { onGetComplete(false, null) }
                    } else {
                        uiThread { onGetComplete(true, response.body()?.string()) }
                    }
                } catch (e: IOException) {
                    Timber.e(e, "Get Request failed")
                    uiThread { onGetComplete(false, null) }
                }
            }
        }
    }

    val getItemsFactory = { http: OkHttpClient, gson: Gson ->
        { onGetItems: (success: Boolean, items: List<Item>?) -> Unit ->
            connect { serverIp ->
                getRequestFactory(http)("$serverIp/items") { success, str ->
                    Timber.d("Result: $success, response: $str")
                    if (!success) {
                        onGetItems(success, null)
                    }
                    else {
                        val response = gson.fromJson(str!!, GetItemsResponse::class.java)
                        onGetItems(response.success, response.items)
                    }
                }
            }
        }
    }
    val getItems = getItemsFactory(httpClient, Gson())
}