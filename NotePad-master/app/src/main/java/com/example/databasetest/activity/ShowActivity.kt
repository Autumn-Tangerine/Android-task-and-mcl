    package com.example.databasetest.activity

import android.content.Intent
import android.os.Bundle
import android.support.v7.widget.Toolbar
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import com.example.databasetest.R
import com.example.databasetest.util.BaseActivity
import com.example.databasetest.util.Utils

class ShowActivity : BaseActivity() {
    private var titleEt: EditText? = null
    private var bodyEt: EditText? = null
    private var timeTv: TextView? = null
    private var button: Button? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_show)
        val toolbar = findViewById<Toolbar>(R.id.toolbar)
        toolbar.title = "日记详情"
        toolbar.setNavigationIcon(R.drawable.backtt)
        toolbar.setNavigationOnClickListener { v ->
            val intent = Intent(v.context, ViewActivity::class.java)
            startActivity(intent)
        }
        timeTv = findViewById(R.id.timeTv)
        titleEt = findViewById(R.id.titleEt)
        bodyEt = findViewById(R.id.bodyEt)
        button = findViewById(R.id.changeBtn)
        val intent = intent
        val title = intent.getStringExtra("title")
        val body = intent.getStringExtra("body")
        val time = intent.getStringExtra("time")
        val id = intent.getIntExtra("id", 1)
        timeTv?.setText("创建日期：$time")
        titleEt?.setText(title)
        bodyEt?.setText(body)
        button?.setOnClickListener(View.OnClickListener { v ->
            val til = titleEt?.getText().toString()
            val bod = bodyEt?.getText().toString()
            val sqLiteDatabase = Utils.getSQLiteDatabase(v.context)
            val sql = "update Notepad set title=?,body=? where id=?"
            sqLiteDatabase.execSQL(sql, arrayOf(til, bod, "" + id))
            Toast.makeText(v.context, "修改成功！", Toast.LENGTH_SHORT).show()
        })
    }
}