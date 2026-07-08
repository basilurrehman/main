/* Scripts */
let debounceTimeout;
document.getElementById('filterInput').addEventListener('input', () => {
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(filterTable, 300);
});

function filterTable() {
  const input = document.getElementById("filterInput").value.toLowerCase();
  const column = document.getElementById("columnSelect").value;
  const table = document.querySelector("table");
  const rows = table.getElementsByTagName("tr");
  const headers = Array.from(table.getElementsByTagName("th"));
  const columnIndex = headers.findIndex(th => th.innerText === column);

  if (columnIndex === -1) return;

  let visibleRowCount = 0;

  for (let i = 1; i < rows.length; i++) {
    const row = rows[i];
    const cell = row.getElementsByTagName("td")[columnIndex];

    if (cell) {
      const text = cell.innerText.toLowerCase();

      if (text.includes(input)) {
        row.style.display = "";
        visibleRowCount++;
        row.getElementsByTagName("td")[0].innerText = visibleRowCount;
      } else {
        row.style.display = "none";
      }
    }
  }
}

function sortTable(columnIndex, order) {
  const table = document.querySelector("table");
  const rows = Array.from(table.rows).slice(1);
  rows.sort((a, b) => {
    const cellA = a.cells[columnIndex].innerText;
    const cellB = b.cells[columnIndex].innerText;
    return order === 'asc' ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
  });
  rows.forEach(row => table.appendChild(row));
}

function toggleMoreContent(button) {
  const moreContent = button.previousElementSibling;
  const visibleContent = moreContent.previousElementSibling;
  if (moreContent.style.display === "none") {
    moreContent.style.display = "inline";
    button.innerText = "Less";
    button.style.display = "block";
  } else {
    moreContent.style.display = "none";
    button.innerText = "More";
    button.style.display = "inline";
  }
}

function toggleAllContent(show) {
  const moreButtons = document.querySelectorAll('.more-button');
  moreButtons.forEach(button => {
    const moreContent = button.previousElementSibling;
    if (show) {
      moreContent.style.display = "inline";
      button.innerText = "Less";
      button.style.display = "block";
    } else {
      moreContent.style.display = "none";
      button.innerText = "More";
      button.style.display = "inline";
    }
  });
}

// Ensure hideAllContent function is defined correctly
function hideAllContent() {
  const moreButtons = document.querySelectorAll('.more-button');
  moreButtons.forEach(button => {
    const moreContent = button.previousElementSibling;
    const visibleContent = moreContent.previousElementSibling;
    moreContent.style.display = "none";
    button.innerText = "More";
    button.style.display = "inline";
    visibleContent.innerText = visibleContent.innerText.slice(0, 20);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const headers = document.querySelectorAll("th");
  headers.forEach((header, index) => {
    header.addEventListener('click', () => {
      const order = header.classList.contains('sort-asc') ? 'desc' : 'asc';
      headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
      header.classList.add(order === 'asc' ? 'sort-asc' : 'sort-desc');
      sortTable(index, order);
    });
  });

  const cells = document.querySelectorAll("td");
  cells.forEach(cell => {
    if (cell.innerText.length > 20) {
      const moreContent = document.createElement("span");
      moreContent.className = "more-content";
      moreContent.innerText = cell.innerText.slice(20);
      const visibleContent = document.createElement("span");
      visibleContent.innerText = cell.innerText.slice(0, 20);
      cell.innerText = "";
      cell.appendChild(visibleContent);
      cell.appendChild(moreContent);
      const moreButton = document.createElement("span");
      moreButton.className = "more-button";
      moreButton.innerText = "More";
      moreButton.onclick = () => toggleMoreContent(moreButton);
      cell.appendChild(moreButton);
      // Add Copy text
      const copyText = document.createElement("span");
      copyText.className = "copy-text";
      copyText.innerText = "Copy";
      copyText.style.cursor = "pointer";
      copyText.onclick = (event) => {
        event.stopPropagation(); // Prevent cell expansion
        const fullText = visibleContent.innerText + moreContent.innerText;
        navigator.clipboard.writeText(fullText);
      };
      cell.appendChild(copyText);
    }
    cell.addEventListener('click', () => {
      const moreContent = cell.querySelector('.more-content');
      const visibleContent = cell.querySelector('span:not(.more-content)');
      if (moreContent && visibleContent) {
        visibleContent.innerText += moreContent.innerText;
        moreContent.remove();
      }
    });
  });

  const filterSection = document.getElementById('filterSection');

  // Show All / Hide All Button
  const showAllButton = document.createElement("button");
  showAllButton.className = "show-all-button";
  showAllButton.innerText = "Show All";
  showAllButton.onclick = () => {
    const show = showAllButton.innerText === "Show All";
    toggleAllContent(show);
    showAllButton.innerText = show ? "Hide All" : "Show All";
  };
  filterSection.appendChild(showAllButton);

  // Add keyboard shortcuts for "Hide All" and "Show All" buttons
  document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'z') {
      event.preventDefault();
      const show = showAllButton.innerText === "Show All";
      toggleAllContent(show);
      showAllButton.innerText = show ? "Hide All" : "Show All";
      // Perform the second toggle
      toggleAllContent(!show);
      showAllButton.innerText = !show ? "Hide All" : "Show All";
    }
  });
});