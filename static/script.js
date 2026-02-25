
document.getElementById("submit_course").addEventListener("click", function() {
    document.getElementById("courseForm").submit(); 
});


document.getElementById("toggleForm").addEventListener("click", function() {
    const form = document.getElementById("coursForm");
    form.style.display = form.style.display === "block" ? "none" : "block";
});

    
document.querySelectorAll(".bloc-matiere").forEach(function(coursDiv) {
  const grade = parseFloat(coursDiv.dataset.grade || 0);
  const barre = coursDiv.querySelector(".remplissage");
  const noteEl = coursDiv.querySelector(".note");

  if (barre) barre.style.width = (grade / 20 * 100) + "%";
  if (noteEl) noteEl.textContent = grade + "/20";
});
