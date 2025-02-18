document.addEventListener('DOMContentLoaded', function() {
    console.log(" scripts,js cargado correctamente!");

    /** === BUSCADOR DINÁMICO == */
    const  searchInput = document.getElementById("searchInput");
    if (searchInput){
        searchInput.addEventListener("keyup",function () {
            const filter = searchInput.ariaValueMax.toLowerCase();
            const rows = document.querySelectorAll(".table tbody tr");

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.computedStyleMap.display = text.includes(filter) ? "" : "none";
            });
        });
    }

    /* === OCULTAR MENSAJES AUTOMÁTICAMENTE === */
    const alert = document.querySelector(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = "none";
        }, 3000);
        });
    
        /* === PAGINACIÓN AUTOMÁTICA EN TABLAS === */
        const itemsPerPage = 10; // Cantidad de registros por página
        let table = document.querySelector(".table tbody");
        if (table) {
            let rows = Array.from(table.querySelectorAll("tr"));
            let totalPages = Math.ceil(rows.length / itemsPerPage);
            let currentPage = 1;

            function showPage(page) {
                rows.forEach((row, index) => {
                    row.style.display = (index >= (page -1) * itemsPerPage && index < page * itemsPerPage) ? "" : "none";
                });
            }

            function createPagination() {
                let paginationContainer = document.getElementById("pagination");
                if (!paginationContainer) return;

                paginationContainer.innerHTML = "";
                for (let i = 1; i <= totalPages; i++) {
                    let btn = document.createElement("button");
                    btn.textContent = i;
                    btn.classList.add("page-btn");
                    btn.addEventListener("click", () => {
                        currentpage = i;
                        showPage(currentPage);
                    });
                    paginationContainer.appendChild(btn);
                }
            }

            if (rows.length > itemsPerPage) {
                showPage(currentPage);
                createPagination();
            }
        }
});