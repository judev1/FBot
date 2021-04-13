window.onscroll = function() {
	if (window.pageYOffset < 30) {
		document.getElementById("menubar").className = "menubar";
	} else {
		document.getElementById("menubar").className = "menubarsmall";
	}
}
function filter() {
	var category, rows, column, i;
	category = document.getElementById("select").value;
	rows = document.getElementsByTagName("tr");
	for (i = 0; i < rows.length; i++) {
		column = rows[i].getElementsByTagName("td")[0];
		if (column.id == category || category == "all") {
			rows[i].style.display = "";
		} else {
			rows[i].style.display = "none";
		}
	}
}
function search() {
	var category, query, rows, column, i, text;
	category = document.getElementById("select").value;
	query = document.getElementById("search").value.toUpperCase();
	rows = document.getElementsByTagName("tr");
	for (i = 0; i < rows.length; i++) {
		column = rows[i].getElementsByTagName("td")[0];
		text = column.textContent;
		if (text.toUpperCase().indexOf(query) > -1 && (column.id == category || category == "all")) {
			rows[i].style.display = "";
		} else {
			rows[i].style.display = "none";
		}      
	}
}