package io.github.assis10t.bobandroid

import android.content.Context
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import java.net.InetAddress

class MainActivity : AppCompatActivity() {

    private val TAG = "MainActivity"

    private var mNsdManager: NsdManager? = null

//    private val SERVICE_TYPE = "_http._tcp."
//    private val SERVICE_NAME = "bob" //TODO: Change to something else.
//    private var mServiceInfo: NsdServiceInfo? = null

//    private val mDiscoveryListener = object : NsdManager.DiscoveryListener {
//
//        // Called as soon as service discovery begins.
//        override fun onDiscoveryStarted(regType: String) {
//            Log.d(TAG, "Service discovery started. regType: $regType")
//        }
//
//        override fun onServiceFound(service: NsdServiceInfo) {
//            // A service was found! Do something with it.
//            Log.d(TAG, "Service discovery success $service")
//            when {
//                service.serviceType != SERVICE_TYPE -> // Service type is the string containing the protocol and
//                    // transport layer for this service.
//                    Log.d(TAG, "Unknown Service Type: ${service.serviceType}")
//                service.serviceName.contains(SERVICE_NAME) -> {
//                    Log.d(TAG, "Resolving service ${service.serviceName}")
//                    mNsdManager!!.resolveService(service, mResolveListener)
//                }
//            }
//        }
//
//        override fun onServiceLost(service: NsdServiceInfo) {
//            // When the network service is no longer available.
//            // Internal bookkeeping code goes here.
//            Log.e(TAG, "service lost: $service")
//        }
//
//        override fun onDiscoveryStopped(serviceType: String) {
//            Log.i(TAG, "Discovery stopped: $serviceType")
//        }
//
//        override fun onStartDiscoveryFailed(serviceType: String, errorCode: Int) {
//            Log.e(TAG, "Discovery failed: Error code:$errorCode")
//            mNsdManager?.stopServiceDiscovery(this)
//        }
//
//        override fun onStopDiscoveryFailed(serviceType: String, errorCode: Int) {
//            Log.e(TAG, "Discovery failed: Error code:$errorCode")
//            mNsdManager?.stopServiceDiscovery(this)
//        }
//    }
//
//    val mResolveListener = object : NsdManager.ResolveListener {
//
//        override fun onResolveFailed(serviceInfo: NsdServiceInfo, errorCode: Int) {
//            // Called when the resolve fails. Use the error code to debug.
//            Log.e(TAG, "Resolve failed: $errorCode")
//        }
//
//        override fun onServiceResolved(serviceInfo: NsdServiceInfo) {
//            Log.e(TAG, "Resolve Succeeded. $serviceInfo")
//            mServiceInfo = serviceInfo
//            val port: Int = serviceInfo.port
//            val host: InetAddress = serviceInfo.host
//
//            Log.v(TAG, "Found service! $host:$port")
//        }
//    }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    override fun onStart() {
        super.onStart()
//        mNsdManager = getSystemService(Context.NSD_SERVICE) as NsdManager
//        mNsdManager!!.discoverServices(SERVICE_TYPE, NsdManager.PROTOCOL_DNS_SD, mDiscoveryListener)

        ServerConnection().connect()
    }
}
