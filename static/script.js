async function extractToken() {
    const cookieInput = document.getElementById("cookieInput").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Extracting token...";

    if (!cookieInput) {
        resultDiv.innerHTML = '<p class="error">Please enter your Facebook cookies.</p>';
        return;
    }

    try {
        const response = await fetch("/extract", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cookies: cookieInput }),
        });

        const data = await response.json();

        if (response.ok) {
            resultDiv.innerHTML = `<p><strong>Access Token:</strong> ${data.access_token}</p>`;
        } else {
            resultDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}
