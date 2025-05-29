// Exemple simple : suppression d’un article via fetch + DOM
document.addEventListener("click", async (e) => {
  if (e.target.matches(".remove-item")) {
    e.preventDefault();
    const url = e.target.href;

    const response = await fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } });
    if (response.ok) {
      // Supprime la ligne du tableau ou recharge
      e.target.closest("tr").remove();
      // Option : mettre à jour le total sans recharger
    } else {
      alert("Erreur lors de la suppression.");
    }
  }
});
