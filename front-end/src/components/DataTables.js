"use client"; // if using Next.js App Router

import { useEffect, useState } from "react";
import { fetchAllData } from "@/app/api/fetchData";

export default function DataTable({ data, handleDelete }) {
    if (!data || data.length === 0) {
      return <p>No Sites are being monitored yet!</p>
    }


    return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Monitored Sites</h1>
      <table className="min-w-full border border-gray-300 rounded-lg shadow">
        <thead className="bg-gray-100">
          <tr>
            <th className="border px-4 py-2 text-left">ID</th>
            <th className="border px-4 py-2 text-left">Name</th>
            <th className="border px-4 py-2 text-left">URL</th>
            <th className="border px-4 py-2 text-left">Interval</th>
            <th className="border px-4 py-2 text-left">Status</th>
            <th className="border px-4 py-2 text-left">Delete</th>
          </tr>
        </thead>
        <tbody>
          {data.map((site) => (
            <tr key={site.id} className="hover:bg-gray-50">
              <td className="border px-4 py-2">{site.id}</td>
              <td className="border px-4 py-2">{site.site_name}</td>
              <td className="border px-4 py-2">{site.site_url}</td>
              <td className="border px-4 py-2">
                {site.intervals.length > 0
                  ? site.intervals.map((i) => i.time_interval).join(", ")
                  : "—"}
              </td>
              <td className="border px-4 py-2">
                {site.statuses.length > 0
                  ? site.statuses.map((s) => (s.status ? "✅ Up" : "❌ Down")).join(", ")
                  : "—"}
              </td>
              <td className="border px-4 py-2"><button onClick={ () => handleDelete(site.id) } className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}