document.addEventListener("DOMContentLoaded", () => {
    const noteInput = document.getElementById("noteInput");
    const saveBtn = document.getElementById("saveBtn");
    const notesList = document.getElementById("notesList");

    // Browser ki LocalStorage se purana data nikalna
    let savedNotes = JSON.parse(localStorage.getItem("myNotes")) || [];
    displayNotes();

    // Data save karne ka function
    saveBtn.addEventListener("click", () => {
        const noteText = noteInput.value.trim();
        if (noteText === "") return;

        savedNotes.push(noteText);
        localStorage.setItem("myNotes", JSON.stringify(savedNotes)); // Browser storage mein save kiya
        
        noteInput.value = ""; // Input box khali kiya
        displayNotes();
    });

    // Notes ko UI par dikhane ka function
    function displayNotes() {
        notesList.innerHTML = "";
        savedNotes.forEach((note, index) => {
            const li = document.createElement("li");
            li.innerHTML = `
                <span>${note}</span>
                <button class="delete-btn" onclick="deleteNote(${index})">❌</button>
            `;
            notesList.appendChild(li);
        });
    }

    // Data delete karne ka function
    window.deleteNote = function(index) {
        savedNotes.splice(index, 1);
        localStorage.setItem("myNotes", JSON.stringify(savedNotes)); // Browser storage update ki
        displayNotes();
    };
});
