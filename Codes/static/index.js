document.getElementById("imageInput").addEventListener("change", function () {
    const fileInput = this.files[0];
    if (fileInput) {
        const formData = new FormData();
        formData.append("image", fileInput);

        fetch("/calculate_size", {
            method: "POST",
            body: formData,
        })
        .then((response) => response.text())
        .then((size) => {
            document.getElementById("result").textContent = `Identified Monument: ${size}`;
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }
});
