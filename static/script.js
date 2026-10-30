const addvareForm = document.querySelector("#add-vare-form");

if (addvareForm) {
  const statusMessage = document.createElement("p");
  statusMessage.setAttribute("role", "status");
  addvareForm.after(statusMessage);

  addvareForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(addvareForm);
    const vare = {
      varenavn: formData.get("name").trim(),
      kategori: formData.get("category"),
      antall_paa_lager: Number(formData.get("quantity")),
      kort_beskrivelse: formData.get("description").trim(),
    };

    try {
      const response = await fetch("/api/nyvare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(vare),
      });
      const result = await response.json();

      statusMessage.textContent = response.ok ? result.message : result.detail;
      if (response.ok) addvareForm.reset();
    } catch {
      statusMessage.textContent = "Kunne ikke kontakte serveren.";
    }
  });
}

const addkategoriForm = document.querySelector("#add-kategori-form");

if (addkategoriForm) {
  const statusMessage = document.createElement("p");
  statusMessage.setAttribute("role", "status");
  addkategoriForm.after(statusMessage);

  addkategoriForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(addkategoriForm);
    const kategori = {
      navn: formData.get("name").trim(),
    };

    try {
      const response = await fetch("/api/kategorier", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(kategori),
      });
      const result = await response.json();

      statusMessage.textContent = response.ok ? result.message : result.detail;
      if (response.ok) addkategoriForm.reset();
    } catch {
      statusMessage.textContent = "Kunne ikke kontakte serveren.";
    }
  });
}

const searchvareForm = document.querySelector("#search-vare-form");
const editvareForm = document.querySelector("#edit-vare-form");

if (searchvareForm && editvareForm) {
  const searchResults = document.querySelector("#search-results");
  const statusMessage = document.createElement("p");
  statusMessage.setAttribute("role", "status");
  editvareForm.after(statusMessage);

  // Fyller ut skjemaet med verdiene til den valgte varen.
  const fyllUtSkjema = (vare) => {
    editvareForm.elements.id.value = vare.id;
    editvareForm.elements.name.value = vare.varenavn;
    editvareForm.elements.category.value = vare.kategori;
    editvareForm.elements.quantity.value = vare.antall_paa_lager;
    editvareForm.elements.description.value = vare.kort_beskrivelse ?? "";
    statusMessage.textContent = "";
    editvareForm.elements.name.focus();
  };

  searchvareForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const sok = new FormData(searchvareForm).get("sok").trim();
    searchResults.replaceChildren();

    try {
      const response = await fetch(`/api/varer?sok=${encodeURIComponent(sok)}`);
      const varer = await response.json();

      if (varer.length === 0) {
        statusMessage.textContent = "Fant ingen varer.";
        return;
      }
      statusMessage.textContent = "";

      // Går rett til redigering hvis det bare er ett treff.
      if (varer.length === 1) {
        fyllUtSkjema(varer[0]);
        return;
      }

      for (const vare of varer) {
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = `#${vare.id} ${vare.varenavn} (${vare.antall_paa_lager} stk)`;
        button.addEventListener("click", () => fyllUtSkjema(vare));
        const item = document.createElement("li");
        item.append(button);
        searchResults.append(item);
      }
    } catch {
      statusMessage.textContent = "Kunne ikke kontakte serveren.";
    }
  });

  editvareForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(editvareForm);
    if (!formData.get("id")) {
      statusMessage.textContent = "Søk opp en vare først.";
      return;
    }
    const vare = {
      varenavn: formData.get("name").trim(),
      kategori: formData.get("category"),
      antall_paa_lager: Number(formData.get("quantity")),
      kort_beskrivelse: formData.get("description").trim(),
    };

    try {
      const response = await fetch(`/api/varer/${formData.get("id")}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(vare),
      });
      const result = await response.json();

      statusMessage.textContent = response.ok ? result.message : result.detail;
      if (response.ok) searchResults.replaceChildren();
    } catch {
      statusMessage.textContent = "Kunne ikke kontakte serveren.";
    }
  });
}

const deleteBtn = document.querySelector(".slett-vare-knapp");

if (deleteBtn && editvareForm) {
  deleteBtn.addEventListener("click", async () => {
    const id = editvareForm.elements.id.value;

    if (!id) {
      alert("Velg en vare først.");
      return;
    }

    const response = await fetch("/api/varer", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: Number(id) }),
    });

    const result = await response.json();

    if (!response.ok) {
      alert(result.detail || "Kunne ikke slette varen.");
      return;
    }

    alert(result.message || "Varen ble slettet.");
    editvareForm.reset();
  });
}
