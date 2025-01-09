function mobileMode() {
    // Get the document element by ID of "mobileMenuArea" 
    var x = document.getElementById("mobileMenuArea");
    // Check if it's displaying a block
    if (x.style.display === "block") {
        // Hide the block
        x.style.display = "none";  
    } else {
        // Show the block
        x.style.display = "block";
    }
}

function updateDepartures() {
    var input = document.getElementById("searchItem"); // Input from user
    var filter = input.value.toUpperCase(); // Input in uppercase
    var table = document.getElementById("departuresBox"); // Table
    var tr = table.getElementsByTagName("tr"); // Row in the table

    for (i = 0; i < tr.length; i++) {
        // Get the element by tag name "td" at 0
        var td = tr[i].getElementsByTagName("td")[0];
        // If data is found
        if (td) {
            var txtValue = td.textContent || td.innerText;
            // Check if the content matches
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                // Display if content matches
                tr[i].style.display = "";
            } else {
                // Hide if content doesn't match
                tr[i].style.display = "none";
            }
        }       
    }
  }

function copyText() {
    // Copy text
    navigator.clipboard.writeText(window.location.href);
}

function mapsClick() {
    // Confirm the user choice
    let confirmation = confirm("This link takes you out of OneTrack. Are you sure you want to leave?")

    // If true, open open train times
    if (confirmation == true) {
        open("https://www.opentraintimes.com/")
    }
}

function confirmSettings() {
    // Confirm user choice
    confirm("Are you sure you want to leave? Any unsaved changes won't be saved.")
}