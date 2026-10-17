const addForm = document.querySelector("#add-form");

const statusMessage = document.createElement("p");
statusMessage.setAttribute("role", "status");
addForm.after(statusMessage);

addForm.addEventListener("submit", async (event) => {
	event.preventDefault();
	const formData = new FormData(addForm);
	const vare = {
		varenavn: formData.get("name").trim(),
		kategori: formData.get("category"),
		antall_paa_lager: Number(formData.get("quantity")),
		kort_beskrivelse: formData.get("description").trim()
	};

	try {
		const response = await fetch("/api/varer", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(vare)
		});
		const result = await response.json();

		statusMessage.textContent = response.ok ? result.message : result.detail;
		if (response.ok) addForm.reset();
	} catch {
		statusMessage.textContent = "Kunne ikke kontakte serveren.";
	}
});