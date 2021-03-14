package com.example.databasetest.ui.home

import android.arch.lifecycle.Observer
import android.arch.lifecycle.ViewModelProvider
import android.content.Intent
import android.os.Bundle
import android.os.Looper
import android.support.v4.app.Fragment
import android.support.v7.widget.Toolbar
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import com.example.databasetest.MediaActivity
import com.example.databasetest.R
import com.example.databasetest.TabActivity
import com.example.databasetest.activity.MainActivity
import com.example.databasetest.activity.ViewActivity

class HomeFragment : Fragment() {

    private lateinit var homeViewModel: HomeViewModel

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        homeViewModel =
                ViewModelProvider(this, ViewModelProvider.NewInstanceFactory()).get(HomeViewModel::class.java)
        val root = inflater.inflate(R.layout.fragment_home, container, false)
        homeViewModel.text.observe(viewLifecycleOwner, Observer {
        })
        return root
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        val toolbar: Toolbar ?= view?.findViewById(R.id.toolbar)
        if (toolbar != null) {
            toolbar.setTitle("缝合怪")
        }
        val alarm:Button?=view?.findViewById(R.id.Alarm)
        view?.findViewById<Button?>(R.id.See)?.setOnClickListener(){
            Log.d("www", "hhh")
            val intent = Intent(activity, ViewActivity::class.java)
            startActivity(intent)
        }
        view?.findViewById<Button?>(R.id.Write)?.setOnClickListener(){
            val intent = Intent(activity, MainActivity::class.java)
            startActivity(intent)
        }
        view?.findViewById<Button?>(R.id.Picture)?.setOnClickListener(){
            val intent= Intent(activity, TabActivity::class.java)
            startActivity(intent)
        }
        view?.findViewById<Button?>(R.id.Media)?.setOnClickListener(){
            val intent= Intent(activity, MediaActivity::class.java)
            startActivity(intent)
        }
        object : Thread() {
            override fun run() {
                try {
                    Looper.prepare()
                    sleep(5000)
                    Toast.makeText(activity, "提醒", Toast.LENGTH_SHORT).show()
                    Looper.loop()
                } catch (e: InterruptedException) {
                    e.printStackTrace()
                }
            }
        }.start()

        val runnable = Runnable {
        }
        view?.findViewById<Button?>(R.id.Alarm)?.setOnClickListener(){
            Thread(runnable).start()
        }
    }
}
