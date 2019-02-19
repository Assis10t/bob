package io.github.assis10t.bobandroid

import android.content.Intent
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.support.v7.widget.CardView
import android.support.v7.widget.GridLayoutManager
import android.support.v7.widget.RecyclerView
import android.view.*
import android.widget.TextView
import io.github.assis10t.bobandroid.pojo.Item
import io.github.assis10t.bobandroid.pojo.Order
import kotlinx.android.synthetic.main.activity_warehouse.*
import timber.log.Timber


class WarehouseActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_warehouse)

        container.isRefreshing = true
        container.setOnRefreshListener { refreshItems() }
        ServerConnection().connect {
            container.isRefreshing = false
        }
        item_list.layoutManager = GridLayoutManager(this, 2)
        item_list.adapter = ItemAdapter { selected ->
            if (selected.isEmpty())
                make_order.hide()
            else
                make_order.show()
        }

        make_order.hide()
        make_order.setOnClickListener {
            container.isRefreshing = true
            make_order.hide()
            val adapter = item_list.adapter as ItemAdapter
            ServerConnection().makeOrder(Order(null, adapter.selectedItems)) { success ->
                if (!success)
                    Timber.e("Could not make order.")
                else {
                    Timber.d("Order made.")
                    refreshItems()
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()

        refreshItems()
    }

    fun refreshItems() {
        container.isRefreshing = true
        ServerConnection().getItems { success, items ->
            container.isRefreshing = false
            if (!success) {
                Timber.e("getItems failed.")
                return@getItems
            }
            Timber.d("GetItems success. Items: ${items?.size}")
            val adapter = item_list.adapter as ItemAdapter
            adapter.updateItems(items!!)
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_toolbar, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle item selection
        return when (item.itemId) {
            R.id.login -> {
                startActivity(Intent(this, LoginActivity::class.java))
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    class ItemAdapter(var onSelectionChanged: (selected: List<Item>) -> Unit): RecyclerView.Adapter<ItemAdapter.ViewHolder>() {
        var itemList: List<Item> = listOf()
        val selectedItems: MutableList<Item> = mutableListOf()
        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context).inflate(R.layout.fragment_warehouse_item, parent, false)
            return ViewHolder(view)
        }

        override fun getItemCount(): Int = itemList.size

        override fun onBindViewHolder(vh: ViewHolder, pos: Int) {
            val item = itemList[pos]
            val context = vh.container.context
            vh.title.text = item.name
            vh.container.setCardBackgroundColor(
                if (selectedItems.contains(item))
                    vh.container.context.getColor(R.color.selectHighlight)
                else
                    vh.container.context.getColor(R.color.white)
            )
            vh.container.cardElevation =
                    if (selectedItems.contains(item))
                        dp(context, 4f)
                    else
                        dp(context, 1f)
            vh.container.setOnClickListener {
                if (selectedItems.contains(item))
                    selectedItems.remove(item)
                else
                    selectedItems.add(item)
                onSelectionChanged(itemList)
                notifyItemChanged(pos)
            }
        }

        fun updateItems(items: List<Item>) {
            this.itemList = items
            this.selectedItems.clear()
            notifyDataSetChanged()
        }

        class ViewHolder(view: View): RecyclerView.ViewHolder(view) {
            val title: TextView = view.findViewById(R.id.title)
            val price: TextView = view.findViewById(R.id.price)
            val container: CardView = view.findViewById(R.id.container)
        }
    }
}
