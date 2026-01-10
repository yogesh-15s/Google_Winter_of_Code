async function analyzeImage() {
    const input = document.getElementById("imageInput");
    const result = document.getElementById("imageResult");

    if (input.files.length === 0) {
        alert("Please select an image");
        return;hi
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    result.innerText = "Analyzing image... ⏳";

    try {
        const response = await fetch("/analyze/image", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        result.innerText =
            `People Count: ${data.people_count} | Density: ${data.density}`;
    } catch (err) {
        result.innerText = "Error analyzing image ❌";
    }
}

async function analyzeVideo() {
    const input = document.getElementById("videoInput");
    const result = document.getElementById("videoResult");

    if (input.files.length === 0) {
        alert("Please select a video");
        return;
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    result.innerText = "Analyzing video... ⏳ (This may take time)";

    try {
        const response = await fetch("/analyze/video", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        result.innerText =
            `Avg People Count: ${data.average_people_count} | Density: ${data.density}`;
    } catch (err) {
        result.innerText = "Error analyzing video ❌";
    }
}
