const form = document.getElementById("emailForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultDiv.style.display = "none";
  resultDiv.innerHTML = "";

  const emailText = document.getElementById("emailInput").value.trim();
  const fileInput = document.getElementById("fileInput").files[0];

  if (!emailText && !fileInput) {
    resultDiv.style.display = "block";
    resultDiv.innerHTML = "<b>Erro:</b> Digite um texto ou envie um arquivo.";
    return;
  }

  try {
    let response;
    if (fileInput) {
      const formData = new FormData();
      formData.append("file", fileInput);

      response = await fetch("/classify-file", {
        method: "POST",
        body: formData
      });
    } else {
      response = await fetch("/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: emailText })
      });
    }

    const data = await response.json();

    if (data.error) {
      resultDiv.style.display = "block";
      resultDiv.innerHTML = `<b>Erro:</b> ${data.error}`;
    } else {
      resultDiv.style.display = "block";
      resultDiv.innerHTML = `
        <p><b>Email:</b> ${data.original_email || "Arquivo enviado"}</p>
        <p><b>Classificação:</b> ${data.category}</p>
      `;
    }
  } catch (err) {
    resultDiv.style.display = "block";
    resultDiv.innerHTML = "<b>Erro:</b> Não foi possível conectar ao servidor.";
  }
});
