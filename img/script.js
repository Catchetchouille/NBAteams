function searchTable() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const table = document.getElementById("myTable");
  const rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName("td");
    let match = false;

    for (let j = 0; j < cells.length; j++) {
      if (cells[j].textContent.toLowerCase().includes(input)) {
        match = true;
        break;
      }
    }

    rows[i].style.display = match ? "" : "none";
  }
}