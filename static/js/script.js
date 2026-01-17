document.addEventListener('DOMContentLoaded', () => {
    console.log("Weather Dashboard Loaded for IP: " + document.body.dataset.ip || "Unknown");

    // Example: Auto-refresh the page every 15 minutes
    setTimeout(() => {
        window.location.reload();
    }, 900000); 
});