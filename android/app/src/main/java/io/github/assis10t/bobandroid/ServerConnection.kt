package io.github.assis10t.bobandroid

<<<<<<< HEAD
import android.os.AsyncTask
import android.util.Log
import java.net.Inet4Address
=======
import com.google.gson.Gson
import io.github.assis10t.bobandroid.pojo.GetItemsResponse
import io.github.assis10t.bobandroid.pojo.Item
import io.github.assis10t.bobandroid.pojo.Order
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import timber.log.Timber
import java.io.IOException
import java.util.concurrent.TimeUnit
>>>>>>> 1339882e609619cd14b45720a5a2a734b8a407d6
import javax.jmdns.JmDNS
import javax.jmdns.ServiceEvent
import javax.jmdns.ServiceListener

class ServerConnection {
<<<<<<< HEAD

    companion object {
        private val TAG = "ServerConnection"
        val SERVER_NAME = "assis10t"
        var serverIp: String? = null

        val onConnectedListeners: MutableList<(String) -> Unit> = mutableListOf()

        class ConnectTask: AsyncTask<Unit, JmDNS, Unit>() {
            override fun doInBackground(vararg params: Unit?) {
                Log.d(TAG, "Discovery started")
                val mJmDNS = JmDNS.create()
                mJmDNS.addServiceListener("_http._tcp.local.", object : ServiceListener {
                    override fun serviceResolved(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Log.d(TAG, "Service resolved: $info")
                        if (info.name.contains(SERVER_NAME)) {
                            serverIp = "${info.inet4Addresses[0]!!.hostAddress}:${info.port}"
                            onConnectedListeners.forEach { it(serverIp!!) }
                            onConnectedListeners.clear()
=======
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
>>>>>>> 1339882e609619cd14b45720a5a2a734b8a407d6
                        }
                    }

                    override fun serviceRemoved(event: ServiceEvent?) {
<<<<<<< HEAD
                        Log.d(TAG, "Service removed")
=======
                        Timber.d("Service removed")
>>>>>>> 1339882e609619cd14b45720a5a2a734b8a407d6
                    }

                    override fun serviceAdded(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
<<<<<<< HEAD
                        Log.d(TAG, "Service added: $info")
                    }
                })
            }
        }

        fun initialize() {
            ConnectTask().execute()
            ServerConnection().connect { ip ->
                Log.d(TAG, "Server found at $ip")
=======
                        Timber.d("Service added: $info")
                    }
                })
            }
            ServerConnection().connect { ip ->
                Timber.d("Server found at $ip")
>>>>>>> 1339882e609619cd14b45720a5a2a734b8a407d6
            }
        }
    }

    fun connect(onConnected: (String) -> Unit) {
<<<<<<< HEAD
        if (serverIp != null)
            onConnected(serverIp!!)
        else
            onConnectedListeners.add(onConnected)
    }
=======
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

    val postRequestFactory = { http: OkHttpClient, gson: Gson ->
        { url: String, body: Any, onPostComplete: (success: Boolean, response: String?) -> Unit ->
            doAsync {
                Timber.d("Post request to $url")
                try {
                    val JSON = MediaType.get("application/json; charset=utf-8")
                    val requestBody = RequestBody.create(JSON, gson.toJson(body))
                    val request = Request.Builder().url(url).post(requestBody).build()
                    val response = http.newCall(request).execute()
                    Timber.d("Response received.")
                    if (!response.isSuccessful) {
                        Timber.e("Post Request failed: (${response.code()}) ${response.body().toString()}")
                        uiThread { onPostComplete(false, null) }
                    } else {
                        uiThread { onPostComplete(true, response.body()?.string()) }
                    }
                } catch (e: IOException) {
                    Timber.e(e, "Post Request failed")
                    uiThread { onPostComplete(false, null) }
                }
            }
        }
    }

    val getItemsFactory = { http: OkHttpClient, gson: Gson ->
        { onGetItems: (success: Boolean, items: List<Item>?) -> Unit ->
            connect { server ->
                getRequestFactory(http)("$server/items") { success, str ->
                    Timber.d("Result: $success, response: $str")
                    if (!success) {
                        onGetItems(success, null)
                    } else {
                        val response = gson.fromJson(str!!, GetItemsResponse::class.java)
                        onGetItems(response.success, response.items)
                    }
                }
            }
        }
    }
    val getItems = getItemsFactory(httpClient, Gson())

    val makeOrderFactory = { http: OkHttpClient, gson: Gson ->
        { order: Order, onOrderComplete: ((success: Boolean) -> Unit)? ->
            connect { server ->
                postRequestFactory(http, gson)("$server/order", order) { success, str ->
                    Timber.d("Result: $success, response: $str")
                    if (!success) {
                        onOrderComplete?.invoke(success)
                    } else {
                        val response = gson.fromJson(str!!, GetItemsResponse::class.java)
                        onOrderComplete?.invoke(response.success)
                    }
                }
            }
        }
    }
    val makeOrder = makeOrderFactory(httpClient, Gson())
>>>>>>> 1339882e609619cd14b45720a5a2a734b8a407d6
}