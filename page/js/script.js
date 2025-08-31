const form = document.getElementById("emailForm");
const resultDiv = document.getElementById("result");
const resultContainer = document.getElementById("resultContainer");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const spinner = document.getElementById("loadingSpinner");


form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultContainer.className = "result hidden";

  const emailText = document.getElementById("emailInput").value.trim();
  const file = fileInput.files[0];

  spinner.classList.remove("hidden");

  if (!emailText && !file) {
    spinner.classList.add("hidden");
    resultContainer.className = "result improdutivo"; 
    resultDiv.innerHTML = "<b>Erro:</b> Digite um texto ou envie um arquivo.";
    return;
  }

  try {
    let response;

    if (file) {
      const formData = new FormData();
      formData.append("file", file);

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

    if (!response.ok || data.error) {
      resultContainer.className = "result improdutivo";
      resultDiv.innerHTML = `<b>Erro:</b> ${data.error || "Falha na classificação."}`;
    } else {
      resultContainer.className = `result ${data.category.toLowerCase()}`;
      resultDiv.innerHTML = `
        <p><b>Email:</b> ${data.original_email || "Arquivo enviado"}</p>
        <p><b>Classificação:</b> ${data.category}</p>
        <p><b>Resposta:</b> ${data.response}</p>
      `;
      document.getElementById("emailInput").value = "";
      fileInput.value = "";
      fileName.textContent = "Nenhum arquivo selecionado";
    }
  } catch (err) {
    resultContainer.className = "result improdutivo";
    resultDiv.innerHTML = "<b>Erro:</b> Não foi possível conectar ao servidor.";
  } finally {
    spinner.classList.add("hidden");
  }
});

document.getElementById("closeResult").addEventListener("click", () => {
  resultContainer.className = "result hidden";
  resultDiv.innerHTML = "";
});

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    fileName.textContent = "Arquivo selecionado: " + fileInput.files[0].name;
  } else {
    fileName.textContent = "Nenhum arquivo selecionado";
  }
});