function mobileMode() {
    var x = document.getElementById("mobileMenuArea");
    if (x.style.display === "block") {
        x.style.display = "none";  
    } else {
        x.style.display = "block";
    }
}

function updateDepartures() {
    var input = document.getElementById("searchItem");
    var filter = input.value.toUpperCase();
    var table = document.getElementById("departuresBox");
    var tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            var txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
            tr[i].style.display = "none";
            }
        }       
    }
  }

/* Copy currentl URL */
function copyText() {
    /*window.alert(window.location.href)*/
    navigator.clipboard.writeText(window.location.href);
}

function mapsClick() {
    let confirmation = confirm("This link takes you out of OneTrack. Are you sure you want to leave?")

    if (confirmation == true) {
        open("https://www.opentraintimes.com/")
    }
}

function confirmSettings() {
    confirm("Are you sure you want to leave? Any unsaved changes won't be saved.")
}

/* 
# TODO Add onclick event to departures to add the clicked item into the search box 
*/
/*
function dimBody() {
    var element = document.getElementById("pageContent");
    if (element.style.opacity === "100%")
        element.style.opacity === "50%"
}
*/