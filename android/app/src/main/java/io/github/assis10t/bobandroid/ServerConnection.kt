package io.github.assis10t.bobandroid

import android.os.AsyncTask
import android.util.Log
import java.net.Inet4Address
import javax.jmdns.JmDNS
import javax.jmdns.ServiceEvent
import javax.jmdns.ServiceListener

class ServerConnection {

    companion object {
        private val TAG = "ServerConnection"
        val SERVER_NAME = "My Web Server"

        class ConnectTask(val onJmDNSCreated: (JmDNS) -> Unit, val onConnected: (Inet4Address, Int) -> Unit): AsyncTask<Unit, JmDNS, Unit>() {
            override fun doInBackground(vararg params: Unit?) {
                Log.d(TAG, "Discovery started")
                val mJmDNS = JmDNS.create()
                publishProgress(mJmDNS)
                mJmDNS.addServiceListener("_http._tcp.local.", object : ServiceListener {
                    override fun serviceResolved(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Log.d(TAG, "Service resolved: $info")
                        if (info.name.contains(SERVER_NAME)) {
                            onConnected(info.inet4Addresses[0], info.port)
                        }
                    }

                    override fun serviceRemoved(event: ServiceEvent?) {
                        Log.d(TAG, "Service removed")
                    }

                    override fun serviceAdded(event: ServiceEvent?) {
                        val info = mJmDNS.getServiceInfo(event!!.type, event.name)
                        Log.d(TAG, "Service added: $info")
                    }
                })
            }
        }
    }

    private var mJmDNS: JmDNS? = null

    fun connect() {
        val connectTask = ConnectTask({mJmDNS = it}) { addr, port ->
            Log.d(TAG, "Server found at ${addr.hostAddress}:$port")
        }
        connectTask.execute()
    }
}