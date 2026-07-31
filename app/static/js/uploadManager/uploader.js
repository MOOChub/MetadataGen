import {loadData} from "../metadataLoader/loadingManager.js";

export async function uploadFile() {
    let file = document.getElementById("file_upload").files[0];

    file = await file.text();
    file = JSON.parse(file);

    file = file["attributes"];

    await loadData(file);
}