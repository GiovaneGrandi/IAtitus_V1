async function sendInput(usuario) {
	const formData = new FormData();
	formData.append("usuario", usuario);

	const response = await fetch("http://127.0.0.1:5000/", {
		method: "POST",
		body: formData,
	});

	if (!response.ok) {
		throw new Error("Erro ao enviar os dados.");
	}
}

document
	.getElementById("contentForm")
	.addEventListener("submit", async function (event) {
		const username = document.getElementById("username").value;
		const password = document.getElementById("password").value;
		let usuario = "";

		if (username == "" || password == "") {
			alert("Por favor, preencha ampos os campos de login.");
			return;
		} else if (username == "professor") {
			usuario = "Professor";
		} else {
			usuario = "Aluno";
		}

		try {
			await sendInput(usuario);
			document.getElementById("contentForm").reset();
		} catch (error) {
			console.error("Erro ao fazer login:", error);
			alert("Erro ao fazer login. Tente novamente.");
		}
	});
