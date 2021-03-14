    package com.example.databasetest.activity

import android.support.v7.app.AlertDialog
import android.content.Intent
import android.os.Bundle
import android.support.v4.widget.SwipeRefreshLayout
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import android.support.v7.widget.Toolbar
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import com.example.databasetest.R
import com.example.databasetest.domain.Note
import com.example.databasetest.util.BaseActivity
import com.example.databasetest.util.Utils
import java.util.*

class ViewActivity : BaseActivity() {
    private val noteList: MutableList<Note> = ArrayList()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_view)
        val swipeRefreshLayout:SwipeRefreshLayout=findViewById(R.id.swipe)
        swipeRefreshLayout.setColorSchemeResources(R.color.colorPrimary)
        swipeRefreshLayout.setOnRefreshListener {
            initNotes()
            Thread.sleep(200)
            swipeRefreshLayout.isRefreshing=false
        }
        val toolbar = findViewById<Toolbar>(R.id.toolbar)
        toolbar.title = "日记一览"
        toolbar.setNavigationIcon(R.drawable.backtt)
        toolbar.setNavigationOnClickListener { v ->
            val intent = Intent(v.context, MainActivity::class.java)
            startActivity(intent)
        }
        initNotes() //初始化日记
        val recyclerView = findViewById<View>(R.id.rv) as RecyclerView
        val layoutManager = LinearLayoutManager(this)
        recyclerView.layoutManager = layoutManager
        val adapter = MyAdapter(noteList)
        recyclerView.adapter = adapter
    }

    private fun initNotes() {
        val sqLiteDatabase = Utils.getSQLiteDatabase(this)
        val cursor = sqLiteDatabase.rawQuery("select * from Notepad", null)
        while (cursor.moveToNext()) {
            val note = Note()
            val string1 = cursor.getString(0)
            val string2 = cursor.getString(1) //标题
            val string3 = cursor.getString(2)
            val string4 = cursor.getString(3) //时间
            note.title = string2
            val parse = Utils.parseDate(string4)
            note.time = parse
            note.body = string3
            note.id = string1.toInt()
            noteList.add(note)
        }
    }
}

internal class MyAdapter(private val noteList: List<Note>) : RecyclerView.Adapter<MyAdapter.ViewHolder>() {
    internal class ViewHolder(var noteView: View) : RecyclerView.ViewHolder(noteView) {
        var noteName: TextView
        var timeTv: TextView

        init {
            timeTv = noteView.findViewById(R.id.timeTv)
            noteName = noteView.findViewById<View>(R.id.note_name) as TextView
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
                .inflate(R.layout.note_item, parent, false)
        val holder = ViewHolder(view)
        holder.noteView.setOnClickListener { v ->
            val position = holder.adapterPosition
            val note = noteList[position]
            val id = note.id
            val sqLiteDatabase = Utils.getSQLiteDatabase(v.context)
            val cursor = sqLiteDatabase.rawQuery("select * from Notepad where id=?", arrayOf("" + id))
            cursor.moveToNext()
            val id2 = cursor.getInt(0)
            val intent = Intent(v.context, ShowActivity::class.java)
            intent.putExtra("title", cursor.getString(1))
            intent.putExtra("body", cursor.getString(2))
            intent.putExtra("time", Utils.getTimeStr(note.time))
            intent.putExtra("id", id2)
            v.context.startActivity(intent)
        }
        holder.timeTv.setOnClickListener { v ->
            val position = holder.adapterPosition
            val note = noteList[position]
            val id = note.id
            val builder = AlertDialog.Builder(v.context)
            builder.setTitle("警告")
            builder.setMessage("您确定要删除该日记吗？")
            builder.setPositiveButton("确定") { dialog, which ->
                val sqLiteDatabase = Utils.getSQLiteDatabase(v.context)
                sqLiteDatabase.execSQL("delete from Notepad where id=?", arrayOf("" + id))
                Toast.makeText(v.context, "删除成功！", Toast.LENGTH_SHORT).show()
            }
            builder.setNegativeButton("取消") { dialog, which -> }
            builder.setCancelable(false)
            val alertDialog = builder.create()
            alertDialog.show()
        }
        return holder
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val note = noteList[position]
        holder.noteName.text = note.title
        val date = note.time
        val timeStr = Utils.getTimeStr(date)
        holder.timeTv.text = timeStr
    }

    override fun getItemCount(): Int {
        return noteList.size
    }
}