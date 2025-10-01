export async function fetchAllData() {
    try {
        const monitoredSites = await fetch("http://127.0.0.1:8000/monitored_sites/fetch")
        if (!monitoredSites.ok) {
            throw new Error("Failed to fetch monitored sites data")
        }
        return await monitoredSites.json()
    } catch (error) {
        console.error("Error fetching data: ", error)
    }
}
