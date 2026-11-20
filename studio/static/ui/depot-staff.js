const copyButton = document.getElementById("copy-invitation");
const invitationUrl = document.getElementById("invitation-url");
const copyStatus = document.getElementById("copy-status");
copyButton.hidden = false;
copyButton.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(invitationUrl.value);
        copyStatus.textContent = "Lien copié.";
    } catch {
        invitationUrl.focus();
        invitationUrl.select();
        copyStatus.textContent = "Le lien est sélectionné. Utilisez la commande Copier de votre appareil.";
    }
});
