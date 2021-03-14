package com.example.databasetest.activity

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.database.sqlite.SQLiteDatabase
import android.os.Bundle
import android.os.Process
import android.support.v4.app.ActivityCompat
import android.support.v7.widget.Toolbar
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import com.example.databasetest.MActivity
import com.example.databasetest.R
import com.example.databasetest.util.ActivityCollector
import com.example.databasetest.util.BaseActivity
import com.example.databasetest.util.Utils
import java.util.*

class MainActivity : BaseActivity(), View.OnClickListener {
    private var titleEt: EditText? = null
    private var bodyEt: EditText? = null
    private var saveBtn: Button? = null
    private var sqLiteDatabase: SQLiteDatabase? = null
    private fun checkPermission() {
        // Storage Permissions
        val REQUEST_EXTERNAL_STORAGE = 1
        val PERMISSIONS_STORAGE = arrayOf(
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE)
        try {
            //检测是否有写的权限
            val permission = ActivityCompat.checkSelfPermission(this@MainActivity,
                    "android.permission.WRITE_EXTERNAL_STORAGE")
            if (permission != PackageManager.PERMISSION_GRANTED) {
                // 没有写的权限，去申请写的权限，会弹出对话框
                ActivityCompat.requestPermissions(this@MainActivity, PERMISSIONS_STORAGE, REQUEST_EXTERNAL_STORAGE)
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val toolbar = findViewById<Toolbar>(R.id.toolbar1)
        toolbar.title = "新建日记"
        toolbar.inflateMenu(R.menu.main)
        toolbar.setOnMenuItemClickListener { item ->
            when (item.itemId) {
                R.id.look -> {
                    val intent = Intent(this@MainActivity, MActivity::class.java)
                    startActivity(intent)
                }
            }
            false
        }
        titleEt = findViewById(R.id.titleEt)
        bodyEt = findViewById(R.id.bodyEt)
        val saveBtn:Button = findViewById(R.id.saveBtn)
        saveBtn.setOnClickListener(this)
        sqLiteDatabase = Utils.getSQLiteDatabase(this)
    }

    override fun onClick(v: View) {
        when (v.id) {
            R.id.saveBtn -> {
                checkPermission()
                val title = titleEt!!.text.toString()
                val body = bodyEt!!.text.toString()
                val date = Date()
                val timeStr = Utils.getTimeStr(date)
                sqLiteDatabase!!.execSQL("insert into Notepad values (?,?,?,?)", arrayOf(null, title, body, timeStr))
                Toast.makeText(this, "保存成功！", Toast.LENGTH_SHORT).show()
            }
            else -> {
            }
        }
    }
}