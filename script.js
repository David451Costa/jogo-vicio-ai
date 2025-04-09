async function buscarDados() {
    const input = document.getElementById("gameInput").value.trim();
    const resultadoDiv = document.getElementById("resultado");

    if (!input) {
        resultadoDiv.innerHTML = "Por favor, insira o nome de um jogo.";
        return;
    }

    resultadoDiv.innerHTML = "Buscando dados...";

    try {
        const response = await fetch("https://addictive-game-meter.onrender.com", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome: input })
        });
        const data = await response.json();

        if (data.erro) {
            resultadoDiv.innerHTML = data.erro;
        } else {
            resultadoDiv.innerHTML = `A pontuação de "${data.nome}" é: <strong>${data.pontuacao}/100</strong>`;
        }
    } catch (error) {
        resultadoDiv.innerHTML = "Erro ao buscar dados.";
        console.error(error);
    }
}
