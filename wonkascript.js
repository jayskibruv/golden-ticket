var submitTicketButton = document.getElementById("submit-ticket")
var getTicketsButton = document.getElementById("get-tickets")
var table = document.getElementById("entrants")
var day = new Date();
var winners = day.getDay()

var sendTicket = function () {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function () {
		if (request.readyState == XMLHttpRequest.DONE) {
			if (request.status >= 200 && request.status < 400) {
				console.log("Request has gone through.");
        entrantName.value = "";
        entrantAge.value = "";
        guestName.value = "";

				var row = table.insertRow(-1);
				var cell1 = row.insertCell(0);
				var cell2 = row.insertCell(1);
				var cell3 = row.insertCell(2);
				cell1.innerHTML = entrant_name;
				cell2.innerHTML = entrant_age;
				cell3.innerHTML = guest_name;

			} else {
				alert("The Oompa Loompas have already received your ticket. Please try again tomorrow.");
		}

	}
	};

	var entrantName = document.getElementById("entrant_name");
	var entrant_name = entrantName.value;
	var entrantAge = document.getElementById("entrant_age");
	var entrant_age = entrantAge.value;
	var guestName = document.getElementById("guest_name")
	var guest_name = guestName.value;
	var data = "entrant_name=" + encodeURIComponent(entrant_name) + "&entrant_age=" + encodeURIComponent(entrant_age) + "&guest_name=" + encodeURIComponent(guest_name);



	request.open("POST","http://localhost:8080/tickets");
	request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	request.withCredentials = true;
	request.send(data);
};

var getTickets = function () {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function () {
		if (request.readyState == XMLHttpRequest.DONE) {
			if (request.status >= 200 && request.status < 400) {
				console.log("Request has gone through.");
				tickets = JSON.parse(request.responseText)
				for (var i=0; i < tickets.length; i++) {

					entrant_id = JSON.parse(request.responseText)
					var ent_id = entrant_id[i]["id"]

          entrants = JSON.parse(request.responseText)
					var entrant_name = entrants[i]["entrant_name"]

          entrants_ages = JSON.parse(request.responseText)
          var entrant_age = entrants_ages[i]["entrant_age"]

          entrants_guests = JSON.parse(request.responseText)
          var guest_name = entrants_guests[i]["guest_name"]

					token_number = JSON.parse(request.responseText)
					var entrant_token = token_number[i]["random_token"]


					var row = table.insertRow(-1);
					row.id = 'r' + ent_id;
					var cell1 = row.insertCell(0);
					var cell2 = row.insertCell(1);
					var cell3 = row.insertCell(2);
				    cell1.innerHTML = entrant_name;
				    cell2.innerHTML = entrant_age;
				    cell3.innerHTML = guest_name;

						if (entrant_token == winners) {
							row.className = "winner"
						}


				}




			} else {
				console.error("Something has gone wrong.");
			}
}
	}

	request.open("GET","http://localhost:8080/tickets");
	request.withCredentials = true;
	request.send();
	console.log(table)
};

function clearTable(table) {
  var rows = table.rows;
  var i = rows.length;
  while (--i) {
    rows[i].parentNode.removeChild(rows[i]);
    // or
    // table.deleteRow(i);
  }
}

submitTicketButton.onclick = function () {
  sendTicket();
	clearTable(table);
	getTickets();

}

window.onload = function() {

	getTickets();
}
