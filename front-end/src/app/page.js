"use client";

import { useState, useEffect } from "react";
import DataTable from "@/components/DataTables";
import { fetchAllData } from "@/app/api/fetchData";
import { deleteData } from "@/app/api/deleteData";


export default function Home() {
  const [sites, setSites] = useState([])
  const [formData, setFormData] = useState({
    apiName: "",
    apiUrl: "",
    interval: "",
  });

  const loadSites = async() => {
    const data = await fetchAllData()
    if (data) setSites(data)
  }

  const handleDelete = async(site_id) => {
    const success = await deleteData(site_id)
    if (success) {
      setSites((prevSites) => prevSites.filter((site) => site.id !== site_id));
    }
  }

  useEffect(() => {
    loadSites()
  }, [])

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async(e) => {
    e.preventDefault()
    try {
      const siteResponse = await fetch("http://127.0.0.1:8000/monitored_sites/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ site_url: formData.apiUrl, site_name: formData.apiName }),
      });
      const newSite = await siteResponse.json();
      const siteId = newSite.id;


      await fetch("http://127.0.0.1:8000/site_check_intervals/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ site_url_id: siteId, time_interval: formData.interval }),
      });


      let isUp = false;
      try {
        await fetch(formData.apiUrl, { mode: "no-cors" });
        isUp = true;
      } catch {
        isUp = false;
      }

      await fetch("http://127.0.0.1:8000/site_status/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ site_url_id: siteId, status: isUp }),
      });

      await loadSites()

      setFormData({
        apiName: "",
        apiUrl: "",
        interval: ""
      })

    } catch (error) {
      console.error("Error creating data: ", error)
    }
    
  };

  return (

    <div className="container">

      {/* Card to allow users to add a new API to track */}
      <div className="flex flex-col items-center gap-4 add-api-card">

        <h1 className="text-xl font-semibold">Network API Monitor</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
              {/* API Name */}
              <div>
                <label className="block text-sm font-medium">API Name</label>
                <input
                  type="text"
                  name="apiName"
                  value={formData.apiName}
                  onChange={handleChange}
                  className="mt-1 w-full border rounded-lg px-3 py-2"
                  required
                />
              </div>

              {/* API URL */}
              <div>
                <label className="block text-sm font-medium">API URL</label>
                <input
                  type="url"
                  name="apiUrl"
                  value={formData.apiUrl}
                  onChange={handleChange}
                  className="mt-1 w-full border rounded-lg px-3 py-2"
                  required
                />
              </div>

              {/* Time Interval */}
              <div>
                <label className="block text-sm font-medium">
                  Time Interval (seconds)
                </label>
                <input
                  type="number"
                  name="interval"
                  value={formData.interval}
                  onChange={handleChange}
                  className="mt-1 w-full border rounded-lg px-3 py-2"
                  required
                  min="1"
                />
              </div>

              {/* Buttons */}
              <div className="flex gap-2 pt-4">
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Add API</button>
              </div>
            </form>
      </div>

      {/* Card for a table showing all of the monitored API's */}
      <div className="flex flex-col items-center gap-4 show-api-card">

        <h1 className="text-xl font-semibold pt-10">All API's</h1>

        <DataTable data = { sites } handleDelete={ handleDelete }/>
      </div>

    </div>
  );
}
