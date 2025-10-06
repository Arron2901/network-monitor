export async function deleteData(site_id) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/monitored_sites/delete?site_id=${site_id}`, {
            method: "DELETE"
        })
        if (!response.ok) {
            throw new Error("Failed to fetch monitored sites data")
        }
        return true
    } catch (error) {
        console.error("Error deleting data: ", error)
        return false
    }
}