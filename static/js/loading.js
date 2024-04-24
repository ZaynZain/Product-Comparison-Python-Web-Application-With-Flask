document.addEventListener("DOMContentLoaded", function() {
  // Hide the loading overlay after 2 seconds
  setTimeout(function(){
    document.body.classList.add('loaded');
    hideLoadingOverlay(); // Call the function to hide the loading overlay
  }, 2000);
});

// Function to show the loading overlay
function showLoadingOverlay() {
  document.getElementById('loading-overlay').classList.add('active');
}

// Function to hide the loading overlay
function hideLoadingOverlay() {
  document.getElementById('loading-overlay').classList.remove('active');
}
