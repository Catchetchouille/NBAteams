function searchTable() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const table = document.getElementById("myTable");
  const rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    const nameCell = rows[i].getElementsByTagName("td")[0];

    if (nameCell) {
      const name = nameCell.innerText.toLowerCase();
      rows[i].style.display = name.includes(input) ? "" : "none";
    }
  }
}